import pyxcc as xcc
import json
import pytest

def test_invalid_option_input():
    with pytest.raises(ValueError) as e:
        option = xcc.Option('o1', ['p1','p1'], [('s1','')])
    assert "Duplicate primary item p1" in str(e.value)
    with pytest.raises(ValueError) as e:
        option = xcc.Option('o1', ['p1','p2'], [('s1',''), ('s1','')])
    assert "Duplicate secondary item s1" in str(e.value)
    with pytest.raises(ValueError) as e:
        option = xcc.Option('o1', ['p1','p2'], [('s1',''), ('p1','')])
    assert "Item p1 both primary and secondary" in str(e.value)
    with pytest.raises(ValueError) as e:
        option = xcc.Option('o1', ['p1'], [('s1','')])
        option.add_primary_item('p1')
    assert "Item p1 overlap with existing primary item" in str(e.value)
    with pytest.raises(ValueError) as e:
        option = xcc.Option('o1', ['p1'], [('s1','')])
        option.add_secondary_item(('s1', 'c'))
    assert "Item s1 overlap with existing secondary item" in str(e.value)

def test_invalid_problem_input():
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p1'], [], [])
    assert "Duplicate primary item p1" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p2'], ['s1', 's1'], [])
    assert "Duplicate secondary item s1" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p2'], ['s1', 'p1'], [])
    assert "Item p1 both primary and secondary" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p2'], [], [
            xcc.Option('o1', ['p1'], []),
            xcc.Option('o1', ['p2'], [])
        ])
    assert "Multiple options with label o1" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p2'], ['s1', 's2'], [])
        problem.add_primary_item('p1')
    assert "Item p1 overlap with existing item" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p2'], ['s1', 's2'], [])
        problem.add_secondary_item('s1')
    assert "Item s1 overlap with existing item" in str(e.value)

def test_invalid_solve_input():
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem([], [], [xcc.Option('o1', ['p1'], [])])
        xcc.solve(problem, True)
    assert "The input problem have no primary items!" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1'], [], [xcc.Option('o1', ['p2'], [])])
        xcc.solve(problem, True)
    assert "Unknown primary item p2 in option" in str(e.value)
    with pytest.raises(ValueError) as e:
        problem = xcc.Problem(['p1', 'p2'], [], [xcc.Option('o1', ['p2'], [])])
        xcc.solve(problem, True)
    assert "Primary p1 not found in options" in str(e.value)

def test_simple_primary_only():
    problem = xcc.Problem(
        ['i1', 'i2', 'i3', 'i4'],
        [],
        [
            xcc.Option('o1', ['i1'], []),
            xcc.Option('o2', ['i1', 'i2', 'i4'], []),
            xcc.Option('o3', ['i3'], []),
            xcc.Option('o4', ['i4'], []),
        ]
    )
    # get all possible solutions
    solutions: xcc.Solutions = xcc.solve(problem, True)
    # one solution found
    assert solutions.count() == 1
    solution = solutions.first()
    # solution with two options
    assert len(solution) == 2
    options = set(solution)
    # options: o2 and o3
    assert options == {'o2', 'o3'}

def test_solve_knuth_a():
    # prepare problem to solve based on
    # binary matrix (Knuth's example)
    # [0, 0, 1, 0, 1, 0, 0],
    # [1, 0, 0, 1, 0, 0, 1],
    # [0, 1, 1, 0, 0, 1, 0],
    # [1, 0, 0, 1, 0, 1, 0],
    # [0, 1, 0, 0, 0, 0, 1],
    # [0, 0, 0, 1, 1, 0, 1],
    problem = xcc.Problem( 
        ['a','b','c','d','e','f','g'], 
        [],
        [
            xcc.Option('r1', ['c', 'e'], []),
            xcc.Option('r2', ['a', 'd', 'g'], []),
            xcc.Option('r3', ['b', 'c', 'f'], []),
            xcc.Option('r4', ['a', 'd', 'f'], []),
            xcc.Option('r5', ['b', 'g'], []),
            xcc.Option('r6', ['d', 'e', 'g'], []),
        ]
    )

    # solve
    solutions: xcc.Solutions = xcc.solve(problem, True)

    # verify
    assert solutions.count() == 1, "1 solution"
    assert len(solutions.first()) == 3, "Solution with 3 rows"
    rows = set(solutions.first())
    assert rows == {'r1', 'r4', 'r5'}, "Solution with rows: 1, 4 and 5"

def test_solve_large():
    # read matrix from file test_matrix.json
    # Running solve on test_matrix.json should give these two solutions:
    # [598, 1945, 2604, 2943, 3171]
    # [819, 2050, 3899, 3965, 4699]
    with open('pytests/test_matrix.json') as f:
        matrix = json.load(f)

    # define problem
    problem = xcc.Problem([], [], [])
    for r in range(0,len(matrix)):
        row = f'{r}'.zfill(4)
        option = xcc.Option(f'o{row}', [], [])
        for i in range(0,len(matrix[r])):
            if r == 0:
                problem.add_primary_item(f'i{i}')
            if matrix[r][i] == 1:
                option.add_primary_item(f'i{i}')
        problem.add_option(option)

    # solve
    solutions: xcc.Solutions = xcc.solve(problem, True)

    # verify
    assert solutions.count() == 2, "2 solutions"
    assert len(solutions.first()) == 5, "Solution with 5 rows"
    assert solutions.first() == ['o0597', 'o1944', 'o2603', 'o2942', 'o3170'], "Solution with rows: 1, 4 and 5"

def test_solve_knuth_b():
    problem = xcc.Problem(
        ['p','q','r'],
        ['x','y'],
        [
            xcc.Option('o1', ['p', 'q'], [('x',''), ('y','a')]),
            xcc.Option('o2', ['p', 'r'], [('x','a'), ('y','')]),
            xcc.Option('o3', ['p'], [('x','b')]),
            xcc.Option('o4', ['q'], [('x','a')]),
            xcc.Option('o5', ['r'], [('y','b')]),
        ]
    )
    # solve
    solutions: xcc.Solutions = xcc.solve(problem, True)

    # verify
    assert solutions.count() == 1, "1 solution"
    assert len(solutions.first()) == 2, "Solution with 5 rows"
    assert solutions.first() == ['o2','o4'], "Solution with rows 2 and 4"

def test_8_queens():
    # construct problem
    problem = xcc.Problem([], [], [])
    # a single queen in each row and column
    for x in range(1,9):
        problem.add_primary_item(f'r{x}')
        problem.add_primary_item(f'c{x}')
    # at most one queen in each diagonal
    for x in range(1,16):
        problem.add_secondary_item(f'u{x}')
        problem.add_secondary_item(f'd{x}')
    # an option for each field on the board
    for x in range(1,9):
        for y in range(1,9):
            problem.add_option(xcc.Option(
                f'{x},{y}',
                [f'r{x}',f'c{y}'], 
                [(f'u{8-x+y}',''),(f'd{x+y-1}','')]
            ))
    
    # solve
    solutions: xcc.Solutions = xcc.solve(problem, True)

    # verify
    assert solutions.count() == 92, "92 solutions"
