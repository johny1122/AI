import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d%s' % i for i in list(range(n_))]  # [d0,..., d(n_ - 1)]
    pegs = ['p%s' % i for i in list(range(m_))]  # [p0,..., p(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"
    # ---- propositions ----
    domain_file.write('Propositions:\n')
    # all disks
    for disk in disks:
        domain_file.write(f'{disk} ')

    # all pegs
    for peg in pegs:
        domain_file.write(f'{peg} ')

    # all pairs of small disk on bigger disk
    for disk1 in range(n_):
        for disk2 in range(disk1 + 1, n_):
            domain_file.write(f'd{disk1}_on_d{disk2} ')

    # all pairs of disk on peg
    for disk in range(n_):
        for peg in range(m_):
            domain_file.write(f'd{disk}_on_p{peg} ')

    # ---- actions ----
    domain_file.write('\nActions:\n')
    # for all disks
    for disk1_size, disk1 in enumerate(disks):
        for peg1 in pegs:
            for peg2 in pegs:
                if peg1 != peg2:
                    write_action(domain_file, disk1, peg1, peg2)  # move disk1 from peg1 to peg2

            for disk2_size in range(disk1_size + 1, n_):
                write_action(domain_file, disk1, peg1, f'd{disk2_size}')  # move disk1 from peg1 to disk2
                write_action(domain_file, disk1, f'd{disk2_size}', peg1)  # move disk1 from disk2 to peg1

        for disk2_size in range(disk1_size + 1, n_):
            for disk3_size in range(disk1_size + 1, n_):
                if disk2_size != disk3_size:
                    write_action(domain_file, disk1, f'd{disk2_size}',
                                 f'd{disk3_size}')  # move disk1 from disk2 to disk3
    domain_file.close()


def write_action(domain_file, disk, source, destination):
    action = f'Name: MOVE_{disk}_from_{source}_to_{destination}\n' + \
             f'pre: {disk} {destination} {disk}_on_{source}\n' + \
             f'add: {source} {disk}_on_{destination}\n' + \
             f'delete: {destination} {disk}_on_{source}\n'
    domain_file.write(action)


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d%s' % i for i in list(range(n_))]  # [d0,..., d(n_ - 1)]
    pegs = ['p%s' % i for i in list(range(m_))]  # [p0,..., p(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"
    # initial
    problem_file.write(f'Initial state: ')
    for peg in pegs[1:]:
        problem_file.write(f'{peg} ')  # all pegs except peg0 are clear

    problem_file.write(f'd0 ')  # disk 0 is clear

    disks_on_one_peg_in_ascending_size_order = ''
    for disk in range(n_ - 1):
        # all disks are one above the other in ascending order of size
        disks_on_one_peg_in_ascending_size_order += f'd{disk}_on_d{disk + 1} '
    problem_file.write(disks_on_one_peg_in_ascending_size_order)
    problem_file.write(f'd{n_ - 1}_on_p0')  # biggest disk is on peg0

    # goal
    problem_file.write(f'\nGoal state: ')
    for peg in pegs[:-1]:
        problem_file.write(f'{peg} ')  # all pegs except peg(m-1) are clear

    problem_file.write(f'd0 ')  # disk 0 is clear

    # all disks are one above the other in ascending order of size
    problem_file.write(disks_on_one_peg_in_ascending_size_order)
    problem_file.write(f'd{n_ - 1}_on_p{m_ - 1}')  # biggest disk is on peg(m-1)

    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
