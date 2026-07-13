
<a id="readme-top"></a>

[![MIT License][license-shield]][license-url]
[![Python 3.10+][python-shield]][python-url]

<br />
<div align="center">
  <a href="https://github.com/acimpoiesu/async-redis-clone">
  </a>

<h3 align="center">async-redis-clone</h3>

  <p align="center">
    A zero-dependency, Python in-memory database made on raw TCP sockets.
    <br />
    <a href="https://github.com/acimpoiesu/async-redis-clone"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/acimpoiesu/async-redis-clone/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/acimpoiesu/async-redis-clone/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

A lightweight, asynchronous key-value store created to natively implement the **Redis Serialization Protocol (RESP)**. 

Rather than relying on any third-party web frameworks or database wrappers, this engine is built from scratch using Python's standard library. It manages multiplexed I/O event loops, intercepts raw byte streams at the transport layer, and executes a custom string-tokenization pipeline to route commands. 

The result is a single-threaded database instance that connects with the official `redis-cli` production tool.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

Runs purely on standard library modules. No `pip install` required.

* [![Python][python-badge]][python-url] (`asyncio`, `socket`)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

You only need Python installed on your machine.
* Python 3.10+
  ```sh
  python --version
  -   (Optional) `redis-tools` for native CLI testing.
    

### Installation

1.  Clone the repo
    
    Bash
    
    ```
    git clone [https://github.com/acimpoiesu/async-redis-clone.git](https://github.com/acimpoiesu/async-redis-clone.git)
    
    ```
    
2.  Navigate to the project directory
    
    Bash
    
    ```
    cd async-redis-clone
    
    ```
    
3.  Boot the server
    
    Bash
    
    ```
    python run.py
    
    ```
    
    _The server will automatically bind and listen on `127.0.0.1:6379`._
    

## Usage

Once the server is running, you can open a separate terminal window and ping the database directly using the native Redis command-line interface:

Bash

```
$ redis-cli
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> SET architecture "hey"
OK
127.0.0.1:6379> GET architecture
"hey"

```

## Roadmap

-   [x] Establish multiplexed socket architecture
    
-   [x] Construct RESP binary deserializer
    
-   [x] Implement base mutating commands (`PING`, `GET`, `SET`)
    
-   [ ] Background min-heap (O(logn)) to track and evict keys based on integer TTLs
    
-   [ ] Build an Append-Only File (AOF) state logger to allow for persistent data recovery
    

See the [open issues](https://github.com/acimpoiesu/async-redis-clone/issues) for a full list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star!

1.  Fork the Project
    
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
    
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
    
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
    
5.  Open a Pull Request
    

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Alexandru Cimpoiesu - [GitHub: @acimpoiesu](https://github.com/acimpoiesu)

Project Link: [https://github.com/acimpoiesu/async-redis-clone](https://github.com/acimpoiesu/async-redis-clone)

## Acknowledgments

-   [Redis Protocol Specification (RESP)](https://redis.io/docs/latest/develop/reference/protocol-spec/)
    
-   [RFC 9112 — HTTP/1.1 (For stream protocol inspiration)](https://datatracker.ietf.org/doc/html/rfc9112)

[license-shield]: https://img.shields.io/github/license/acimpoiesu/async-redis-clone.svg?style=for-the-badge
[license-url]: https://github.com/acimpoiesu/async-redis-clone/blob/main/LICENSE.txt
[python-shield]: https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white