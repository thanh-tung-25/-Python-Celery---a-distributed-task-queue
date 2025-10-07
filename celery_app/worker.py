from . import app

if __name__ == '__main__':
    # Cách đơn giản để chạy worker khi gọi file này trực tiếp:
    app.worker_main(argv=['worker', '--loglevel=info'])
