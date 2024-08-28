# ObfusGuard Encoding and Hashing Algorithm

**ObfusGuard** is a non-cryptographic, multi-layered Encoding and Hashing algorithm designed to provide simple obfuscation and hashing for text input. It consists of three levels of encoding and a hashing function that transforms the input message into a non-reversible hash. The algorithm is implemented in Python and can be used to encode and hash text messages for basic security purposes. This algorithm is suitable for educational purposes or lightweight obfuscation but should not be used for applications requiring strong cryptographic security.

## Features

- **Multi-Layered Encoding**: Three levels of encoding increase the complexity of the transformation.
- **Fixed Size Hashing**: The final hash is a fixed size, regardless of the input message length, making it suitable for storing in databases and hard to reverse-engineer.

## How It Works

1. **Level One Encoding**: Each character in the message is mapped to a sequence of digits using `KMAP`.
2. **Level Two Encoding**: Each digit in the encoded message is then mapped to an alphabetic character using `ALOHA_MAP`.
3. **Level Three Encoding**: Sequences of repeated characters are compressed into a count followed by the character itself.
4. **Final Hash**: The final message undergoes a second transformation using `ALOPHA_MAP` to produce a non-reversible hash. The hash is a fixed size of 32 characters regardless of the input message length.
<!-- 
# ObfusGuard

ObfusGuard is a Python package that provides multilevel Encoding and hashing.

## Installation

```bash
pip install ObfusGuard -->
