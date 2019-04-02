def boxplot_params(data, lam):
    data.sort()
    n = len(data)
    lower_whisker = data[0] * 2 * lam
    lower_quartile = data[n//4] * 2 * lam
    median = data[n // 2] * 2 * lam
    upper_quartile = data[n * 3 // 4] * 2 * lam
    upper_whisker = data[-1] * 2 * lam
    return lower_whisker, lower_quartile, median, upper_quartile, upper_whisker


data1 = dict() # keys -- lambdas
data2 = dict() # keys -- lambda_mut
with open('one-plus-lambda-lambda.out', 'r') as f:
    lines = f.readlines()
    for i in range(9):
        data1[2 ** i] = [int(s) for s in lines[2 * i + 1].split()]
    for i in range(9):
        data2[2 ** i] = [int(s) for s in lines[2 * i + 19].split()]


def draw_plot_equal_lambda():
    print('\\begin{tikzpicture}')
    print('\\begin{axis}[')
    print('\tboxplot/draw direction=y,')
    print('\tx axis line style={opacity=0},')
    print('\txlabel=$\lambda$,')
    print('\tylabel=Fitness evaluations,')
    print('\taxis x line*=bottom,')
    print('\taxis y line=left,')
    print('\tenlarge y limits,')
    print('\tymajorgrids,')
    print('\txtick={{{}}},'.format(', '.join([str(i) for i in range(1, 10)])))
    print('\txticklabels={{{}}},'.format(', '.join([str(2 ** i) for i in range(9)])))
    print('\t/pgfplots/boxplot/whisker range={3},')
    print('\t/pgfplots/boxplot/every box/.style={solid},')
    print('\t/pgfplots/boxplot/every whisker/.style={solid},')
    print('\t/pgfplots/boxplot/every median/.style={solid,thick},')
    print(']')

    for i in range(9):

        data1[2 ** i].sort()
        print('\t\\addplot+ [boxplot]')
        print('\t\ttable [row sep=\\\\,y index=0] {')
        print('\t\t\tdata\\\\')
        print('\t\t\t{}\\\\'.format('\\\\ '.join(str(2 * s * 2 ** i) for s in data1[2 ** i])))
        print('\t};')

    print('\\end{axis}')
    print('\\end{tikzpicture}')


def draw_plot_different_lambda():
    print('\\begin{tikzpicture}')
    print('\\begin{axis}[')
    print('\tboxplot/draw direction=y,')
    print('\tx axis line style={opacity=0},')
    print('\txlabel=$\lambda_{m}$,')
    print('\tylabel=Fitness evaluations,')
    print('\taxis x line*=bottom,')
    print('\taxis y line=left,')
    print('\tenlarge y limits,')
    print('\tymajorgrids,')
    print('\txtick={{{}}},'.format(', '.join([str(i) for i in range(1, 11)])))
    print('\txticklabels={{$\\lambda_{{m}} = 1 \\atop \\lambda_{{x}} = 1$, {}}},'.format(', '.join([str(2 ** i) for i in range(9)])))
    print('\t/pgfplots/boxplot/whisker range={3},')
    print('\t/pgfplots/boxplot/every box/.style={solid},')
    print('\t/pgfplots/boxplot/every whisker/.style={solid},')
    print('\t/pgfplots/boxplot/every median/.style={solid,thick},')
    print(']')

    data1[1].sort()
    print('\t\\addplot+ [boxplot]')
    print('\t\ttable [row sep=\\\\,y index=0] {')
    print('\t\t\tdata\\\\')
    print('\t\t\t{}\\\\'.format('\\\\ '.join(str(s) for s in data1[1])))
    print('\t};')

    for i in range(9):
        data2[2 ** i].sort()
        print('\t\\addplot+ [boxplot]')
        print('\t\ttable [row sep=\\\\,y index=0] {')
        print('\t\t\tdata\\\\')
        print('\t\t\t{}\\\\'.format('\\\\ '.join(str(3 * s * 2 ** i) for s in data2[2 ** i])))
        print('\t};')

    print('\\end{axis}')
    print('\\end{tikzpicture}')


def draw_plots_together():
    print('\\begin{tikzpicture}')
    print('\\begin{axis}[')
    print('\tboxplot/draw direction=y,')
    print('\tx axis line style={opacity=0},')
    print('\txlabel=$\lambda$,')
    print('\tylabel=Fitness evaluations,')
    print('\taxis x line*=bottom,')
    print('\taxis y line=left,')
    print('\tenlarge y limits,')
    print('\tymajorgrids,')
    print('\txtick={{{}}},'.format(', '.join([str(i) for i in range(19)])))
    print('\txticklabels={{\\footnotesize{{$\\lambda_{{m}} \\atop \\lambda_{{x}}$}}, {}}},'.format(', '.join(["\\footnotesize{{${} \\atop {}$}}".format(str(2 ** (i // 2)), str(2 ** ((i + 1) // 2))) for i in range(18)])))
    print('\t/pgfplots/boxplot/whisker range={3},')
    print('\t/pgfplots/boxplot/every box/.style={solid},')
    print('\t/pgfplots/boxplot/every whisker/.style={solid},')
    print('\t/pgfplots/boxplot/every median/.style={solid,thick},')
    print(']')



    for i in range(9):
        data1[2 ** i].sort()
        print('\t\\addplot+ [boxplot]')
        print('\t\ttable [row sep=\\\\,y index=0] {')
        print('\t\t\tdata\\\\')
        print('\t\t\t{}\\\\'.format('\\\\ '.join(str(2 * s * 2 ** i) for s in data2[2 ** i])))
        print('\t};')


        data2[2 ** i].sort()
        print('\t\\addplot+ [boxplot]')
        print('\t\ttable [row sep=\\\\,y index=0] {')
        print('\t\t\tdata\\\\')
        print('\t\t\t{}\\\\'.format('\\\\ '.join(str(3 * s * 2 ** i) for s in data2[2 ** i])))
        print('\t};')

    print('\\end{axis}')
    print('\\end{tikzpicture}')


draw_plot_different_lambda()