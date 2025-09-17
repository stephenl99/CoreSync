extern "C" {
#include <base/log.h>
}

#include "runtime.h"
#include "sync.h"
#include "synthetic_worker.h"
#include "thread.h"
#include "timer.h"
#include <sys/shm.h>
#include <unistd.h>
#include <errno.h>
#include <chrono>
#include <iostream>
#include <iomanip>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

barrier_t barrier;

bool synth_barrier_wait() { return barrier_wait(&barrier); }

namespace {

std::string mode;
int SHM_KEY;
int threads;
uint64_t n;
std::string worker_spec;
double duration;

void MainHandler(void *arg) {

    uint64_t* cnt;
    log_info("SHM_KEY: %d, threads: %d\n", SHM_KEY, threads);
    int shm_id = shmget((key_t) SHM_KEY, 0, 0600);
    if (shm_id == -1) {
        log_err("failed to get shm_id from key: %d in stress.cc", SHM_KEY);
        printf("Something went wrong with shmget()! %s\n", strerror(errno));
        printf("actual errno: %d\n", errno);
        exit(1);
    }
    void* shm_ptr = shmat(shm_id, 0, 0);
    if (shm_ptr == (void*) -1) {
        log_err("failed to get shm_id in stress.cc");
        exit(1);
    }
    cnt = (uint64_t*) shm_ptr;

    rt::WaitGroup wg(1);

    barrier_init(&barrier, threads);

    for (int i = 0; i < threads; ++i) {
        rt::Spawn([&, i]() {
                auto *w = SyntheticWorkerFactory(worker_spec);
                if (w == nullptr) {
                    std::cerr << "Failed to create worker." << std::endl;
                    exit(1);
                }

                cnt[i] = 0;
                while (true) {
                    w->Work(n);
                    cnt[i]++;
                    rt::Yield();
                }
            });
    }

    // never returns
    wg.Wait();
}

}  // anonymous namespace

int main(int argc, char *argv[]) {
  int ret;

  if (argc < 3) {
      printf("usage: [config] [init/work/dump/deinit] [additional args...]\n");
      return -1;
  }

  mode = std::string(argv[2]);

  if (mode == "init") {
      if (argc != 5) {
          printf("usage: [config] [init] [SHM_KEY] [#threads]\n");
          return -1;
      }
      SHM_KEY = std::stoi(argv[3]);
      threads = std::stoi(argv[4]);

        int shm_id = shmget((key_t) SHM_KEY, sizeof(uint64_t)*threads, IPC_CREAT | 0600);
        if (shm_id == -1) {
            printf("Failed to create the shared memory region: %s\n", strerror(errno));
            return -1;
        }
        void* shm_ptr = shmat(shm_id, 0, 0);
        if (shm_ptr == (void *)-1) {
            printf("Failed to attach the shared memory region: %s\n", strerror(errno));
            return -1;
        }
        uint64_t *cnt = (uint64_t *)shm_ptr;
        for (int i = 0; i < threads; i++) {
            cnt[i] = 0;
        }

        // Block forever
        int ret;
        int pipefd[2];
        ret = pipe(pipefd);
        if (ret == -1) {
            printf("Failed to create a pipe\n");
            return -1;
        }
        char dummy;
        ret = read(pipefd[0], &dummy, sizeof(char));
        if (ret <= 0) {
            printf("Read on a pipe failed\n");
            return -1;
        }

        return 0;

  } else if (mode == "deinit") {
      if (argc != 4) {
          printf("usage: [config] [deinit] [SHM_KEY]\n");
          return -1;
      }
      SHM_KEY = std::stoi(argv[3]);

      int shm_id = shmget((key_t) SHM_KEY, 0, 0600);
      if (shm_id == -1) {
          printf("Failed to get the shared memory region: %s\n", strerror(errno));
          return -1;
      }
      shmctl(shm_id, IPC_RMID, NULL);
      return 0;

  } else if (mode == "dump") {
      if (argc != 6) {
          printf("usage: [config] [dump] [SHM_KEY] [#threads] [duration]\n");
          return -1;
      }
      SHM_KEY = std::stoi(argv[3]);
      threads = std::stoi(argv[4]);
      duration = std::stod(argv[5]);

      int shm_id = shmget((key_t) SHM_KEY, 0, 0600);
      if (shm_id == -1) {
          printf("Failed to get the shared memory region: %s\n", strerror(errno));
          return -1;
      }
      assert(shm_id != -1);
      void* shm_ptr = shmat(shm_id, 0, 0);
      if (shm_ptr == (void *)-1) {
          printf("Failed to attach the shared memory region: %s\n", strerror(errno));
          return -1;
      }
      uint64_t* cnt = (uint64_t *)shm_ptr;
      uint64_t total = 0;
      for (int i = 0; i < threads; i++) {
          total += cnt[i];
      }
      printf("%lf, %lf\n", (double)total/duration, duration);
      shmdt(shm_ptr);
      return 0;

  } else if (mode == "work") {
      if (argc != 7) {
          printf("usage: [config] [work] [SHM_KEY] [#threads] [#work_units] [#work_spec]\n");
          return -1;
      }
      SHM_KEY = std::stoi(argv[3]);
      threads = std::stoi(argv[4]);
      n = std::stoul(argv[5], nullptr, 0);
      worker_spec = std::string(argv[6]);

      std::cout << std::setprecision(8) << std::fixed;

      ret = runtime_init(argv[1], MainHandler, NULL);
      if (ret) {
          printf("failed to start runtime\n");
          return ret;
      }

      return 0;

  } else {
      printf("usage: [config] [init/work/dump/deinit] [additional args...]\n");
      return -1;
  }

  return 0;
}
