CODE = "(add 2 (subtract 4 2))"
BUILTINS = { 
        '>': 'infix',
        '<': 'infix',
        'if': 'prefix', 
        'for': 'prefix',
        'true': 'value', 
        'false': 'value'
        } 

class Cursor():
    def __init__(self, cnt=0):
        self.count = cnt
    def increment(self):
        self.count += 1
    def __gt__(self, num):
        return self.count > num
    def __lt__(self, num):
        return self.count < num


def tokenizer(code):
    current = 0
    tokens = list()
    while current < len(code):
        char = code[current]
        if char == '(':
            tokens.append({
                'type':'paren',
                'value':'('
                })
            current += 1
            continue
        if char == ')':
                tokens.append({
                    'type':'paren',
                    'value':')'
                    })
                current += 1
                continue
        if char.isspace():
            current += 1
            continue
        builtin = BUILTINS.get(char, False)
        if builtin:
            current += 1
            tokens.append({
                'type': BUILTINS[char],
                'value': char 
                })
            continue
        if char <= '9' and char >= '0' or char == '.':
            value = ''
            while char <= '9' and char >= '0' or char == '.':
                value += char
                current += 1
                char = code[current]
            tokens.append({
                'type':'number',
                'value':value
                })
            continue
        if char.isalpha():
            value = ''
            while char.isalpha():
                value += char
                current += 1
                char = code[current]
            builtin = BUILTINS.get(value, False)
            if builtin:
                tokens.append({
                    'type': BUILTINS[value],
                    'value': value
                    })
            else:
                tokens.append({
                    'type':'name',
                    'value':value
                    })
            continue
        else:
            raise ValueError('I don\'t know what this character is:{}'.format(char))

    return tokens

def parser(tokens):
    current = Cursor() 
    def walk(tokens, current):
        token = tokens[current.count]
        if token['type'] == 'number':
            current.increment()
            return {
                'type':'NumberLiteral',
                'value':token['value']
                }

        if token['type'] == 'paren' and token['value'] == '(':
            current.increment()
            token = tokens[current.count]
            node = {
                'type':'CallExpression',
                'name':token['value'],
                'params':[]
                }
            current.increment()
            token = tokens[current.count]
            while token['type'] != 'paren' or  \
                    (token['value'] != ')' and token['type'] == 'paren'):
                node['params'].append(walk(tokens, current))
                token = tokens[current.count]
            current.increment()
            return node
        else:
            raise ValueError("Unknown type:{}".format(token['type']))
    ast = {
            'type':'Program',
            'body':[]
            }
    while current < len(tokens):
        ast['body'].append(walk(tokens, current))
    return ast

def traverser(ast, visitor):
    def traverse_array(array, parent):
        map(lambda x: traverse_node(x, parent), array)
    def traverse_node(node, parent):
        if node['type'] == 'Program':
            traverse_array(node['body'], node)
        elif node['type'] == 'CallExpression':
            method = visitor[node['type']]
            method(node, parent)
            traverse_array(node['params'], node)
        elif node['type'] == 'NumberLiteral':
            method = visitor[node['type']]
            method(node, parent)
        else:
            raise ValueError('Unknown type: {}'.format(node['type']))
    traverse_node(ast, None)

def transformer(ast):
    newAst = {
            'type':'Program',
            'body':[]
            }
    ast['context'] = newAst['body']
    def add_node(node, parent):
        parent['context'].append({
            'type':'NumberLiteral',
            'value': node['value']
            })
    def call_expression(node, parent):
        builtin = BUILTINS.get(node.get('name',''), False)
        if not builtin:
            expression = {
                        'type':'CallExpression',
                        'callee':{
                            'type':'Identifier',
                            'name':node['name']
                            },
                        'arguments':[]
                        }
        else:
            expression = {
                    'type':'CallExpression',
                    'callee':{
                        'type':'Builtin',
                        'name':node['name']
                        },
                    'arguments':[]
                    }
        node['context'] = expression['arguments']
        if parent['type'] != 'CallExpression':
            expression = {
                    'type':'ExpressionStatement',
                    'expression': expression
                    }
        parent['context'].append(expression) 
    traverser(ast, {
        'NumberLiteral': add_node,
        'CallExpression': call_expression
        })
    return newAst

def code_generator(node):
    if node['type'] == 'Program':
        return '\n'.join(map(code_generator, node['body']))
    elif node['type'] == 'ExpressionStatement':
        return code_generator(node['expression']) # +';'
    elif node['type'] == 'CallExpression':
        if node['callee']['type'] == 'Identifier':
            return code_generator(node['callee']) + \
                    '(' + ', ' \
                    .join(map(code_generator, node['arguments'])) + \
                    ')'
        elif node['callee']['type'] == 'Builtin':
            if BUILTINS[node['callee']['name']] == 'prefix':
                return code_generator(node['callee']) + ' '+\
                        ':\n '.join(map(code_generator, node['arguments']))
            elif BUILTINS[node['callee']['name']] == 'infix':
                return code_generator(node['arguments'][0])+\
                        code_generator(node['callee'])+\
                        code_generator(node['arguments'][1])
    elif node['type'] == 'Identifier':
        return node['name']
    elif node['type'] == 'Builtin':
        return node['name']
    elif node['type'] == 'NumberLiteral':
        return node['value']
    else:
        raise ValueError('Unknown type: {}'.format(node['type']))

def compiler(code):
    tokens = tokenizer(code)
    ast = parser(tokens)
    newAst = transformer(ast)
    output = code_generator(newAst)
    return output

def main():
    def add(n, k):
        return n + k
    def subtract(i, j):
        return i - j
    print(eval(compiler(CODE)))

if __name__ == "__main__":
    main()
