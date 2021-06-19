#!/usr/bin/env python3

import os

class LinearProblem:
    '''
        Construtor
        Iniciando os Jobs e Machines
    '''
    def __init__(self):
        self.tasks = []
        self.machines = []

    def read_input(self):
        '''
            input() -> '2 2' -> split(' ') -> ['2', '2'] -> map(int, ['2', '2']) -> [2, 2]
        '''
        job_amount, machines_amount = map(int, input().split(' '))

        for i in range(0, job_amount):
            self.tasks.append(dict(
                index=i+1,
                time=int(input())
            ))
        
        for i in range(0, machines_amount):
            cost_amount, max_time = map(int, input().split(' '))
            self.machines.append(dict(
                index=i+1,
                cost=cost_amount,
                max_time=max_time
            ))

        for machine in self.machines:
            machine_tasks = int(input())
            machine['tasks'] = []
            for i in range(0, machine_tasks):
                machine['tasks'].append(int(input()))

    def calculate_cost(self):
        operation_cost = 'min: '
        for machine in self.machines:
            for task in self.tasks:
                machine_cost, machine_index, task_index = machine['cost'], machine['index'], task['index']
                operation_cost += f'{machine_cost} h{machine_index}{task_index} + '
        self.operation_cost = operation_cost[:-3] + ';\n'

        self.machine_functions = []
        for machine in self.machines:
            index, max_time = machine['index'], machine['max_time']
            machine_function = ''
            for task in machine['tasks']:
                machine_function += f'h{index}{task} + '
            machine_function = machine_function[:-3]
            machine_function += f' <= {max_time};\n'
            self.machine_functions.append(machine_function)

        self.task_fuctions = []
        for task in self.tasks:
            job_index, time = task['index'], task['time']
            task_function = ''
            for machine in self.machines:
                machine_index = machine['index']
                task_function += f'h{machine_index}{job_index} + '
            task_function = task_function[:-3]
            task_function += f' = {time};\n'
            self.task_fuctions.append(task_function)
        
        self.restriction_functions = []
        for machine in self.machines:
            machine_index, machine_tasks = machine['index'], machine['tasks']
            for task in self.tasks:
                task_index = task['index']
                if task_index in machine_tasks:
                    restriction_function = f'h{machine_index}{job_index} >= 0;\n'
                else:
                    restriction_function = f'h{machine_index}{job_index} = 0;\n'
                self.restriction_functions.append(restriction_function)

    def save_inputs(self):
        file = open('temp/model.lp', 'w')
        file.write(self.operation_cost)
        for machine_function in self.machine_functions:
            file.write(machine_function)
        for task_function in self.task_fuctions:
            file.write(task_function)
        for restriction_function in self.restriction_functions:
            file.write(restriction_function)
        file.close()

    def execute_external_lib(self):
        os.system('lp_solve temp/model.lp > temp/output.txt')

    def read_outputs(self):
        file = open('temp/output.txt', 'r')
        self.amount = 0
        self.tasks_amount = {}
        # salva os valores dos lp_solve em variaveis
        for i, line in enumerate(file):
            if i == 1:
                self.amount = float(line.split(' ')[-1])
            elif i > 3:
                line_items = line.split(' ')
                task_amount = line_items[-1].replace('\n', '')
                self.tasks_amount[line_items[0]] = task_amount
        file.close()

    def show_result(self):
        # salva os valores do tempo de cada tarefa nas maquinas correspondentes
        for machine in self.machines:
            machine_index = machine['index']
            machine['amounts'] = []
            for task in self.tasks:
                task_index = task['index']
                index = f'h{machine_index}{task_index}'
                machine['amounts'].append({index: self.tasks_amount.get(index, 0)})

        # imprime os resultados, uma linha por maquina e uma coluna por tarefa
        output_string = ''
        for machine in self.machines:
            for task_amount in machine['amounts']:
                for key in task_amount.keys():
                    output_string += f'{float(task_amount.get(key))} '
            output_string = output_string[:-1] + '\n'

        output_string += str(self.amount)
        print(output_string)

    '''
        Método que executa a solução do problema
    '''
    def solve(self):
        self.read_input()
        self.calculate_cost()
        self.save_inputs()
        self.execute_external_lib()
        self.read_outputs()
        self.show_result()

if __name__ == '__main__':
    linear_problem = LinearProblem()
    linear_problem.solve()
