#!/bin/env python
"""Test docker image."""
import docker


client = docker.from_env()
c = client.containers.run(
    image="sphere",
    command=["vv"],
    stdin_open=True,
    detach=True,
)
s = c.attach_socket(params={"stdin": 1, "stream": 1, "stdout": 1, "stderr": 1})
x = input() + "\n"
print(x)
s._sock.sendall(x.encode("utf-8"))  # pylint: disable=protected-access
c.wait()
stdout = c.logs(stdout=True, stderr=False).decode("utf-8")
c.remove()
print(stdout)
