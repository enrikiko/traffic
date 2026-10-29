from fastapi import FastAPI

app = FastAPI()

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/fibonacci/{n}')
def fibonacci(n: int):
    if n < 0 or n > 100:
        return {'error': 'n must be between 0 and 100'}
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return {'n': n, 'value': str(a)}
