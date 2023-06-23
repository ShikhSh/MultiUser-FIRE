from MainAlgo.run import Runner_main
from Baseline1.run import Runner_BL1
from Baseline2.run import Runner_BL2
from Baseline3.run import Runner_BL3

if __name__ == '__main__':
    runner_main = Runner_main()
    runner_main.run_program()

    runner_bl3 = Runner_BL3()
    runner_bl3.run_program()

    runner_bl2 = Runner_BL2()
    runner_bl2.run_program()

    runner_bl1 = Runner_BL1()
    runner_bl1.run_program()