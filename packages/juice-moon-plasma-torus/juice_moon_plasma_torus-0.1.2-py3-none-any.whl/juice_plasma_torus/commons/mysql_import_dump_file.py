"""
Created on January 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to import a mysql dump file
"""


def import_dump_file(input_dump_file, db_name, db_user, db_pass):
    """
    Import Mysql dump file in database

    :param input_dump_file: input sql dump file
    :param db_name: database nanme
    :param db_user: user name
    :param db_pass: password
    """

    import subprocess

    command = 'time mysql -u{} -p{} {} < {}'.format(db_user, db_pass, db_name, input_dump_file)
    print('command: {}\n'.format(command))

    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while True:
            
            lines = p.stdout.readlines()
            
            if not lines:
                break
                
            elif 'Error' in '{}'.format(lines):
                print('error: {}'.format(lines))

            else:
                for line in lines:
                    print('{}'.format('\t{}'.format(line.decode("utf-8").replace('\n', ''))))

        p.wait()

        if p.returncode != 0:
            print(p.returncode, p.stdout, p.stderr)
            p.terminate()

        print('\nExecution completed!')
        print('Sql dump file {} imported in databse {}'.format(input_dump_file, db_name))

    except Exception as e:

        print(str(e))