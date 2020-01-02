import polling


def wait_until(condition, step=1, timeout=30):
    polling.poll(
        lambda: condition,
        step=step,
        timeout=timeout,
    )
