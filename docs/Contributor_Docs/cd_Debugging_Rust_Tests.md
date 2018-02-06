# <a name="Top"></a>Debugging Rust Tests

[**Software Contributor Documentation Table of Contents**](cd_TOC.md)

![rust-debug](md_Graphics/rust-debug.jpg)

There are some cases (especially when working with c level bindings) where you'd like
to jump into a gdb session to debug a failing Rust test.

This guide will walk through that process.

1. Identify the failing test. You can do this with `cargo test` in the directory. You will see something like:

```shell
[root@localhost libzfs]# cargo test
   Compiling libzfs v0.5.0 (file:///vagrant/libzfs)
    Finished dev [unoptimized + debuginfo] target(s) in 7.52 secs
     Running /vagrant/target/debug/deps/libzfs-37d0dad38d98d030

running 2 tests
test tests::import_check_methods_export ... FAILED
test tests::open_close_handle ... ok

failures:

---- tests::import_check_methods_export stdout ----
    [Zpool { raw: 0x7f0ead8d9000 }]
thread 'tests::import_check_methods_export' panicked at 'called `Result::unwrap()` on an `Err` value: Io(Error { repr: Os { code: -1, message: "Unknown error -1" } })', /checkout/src/libcore/result.rs:906:4
note: Run with `RUST_BACKTRACE=1` for a backtrace.


failures:
    tests::import_check_methods_export

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out

error: test failed, to rerun pass '--lib'
```

The line `Running /vagrant/target/debug/deps/libzfs-37d0dad38d98d030` shows where the file lives.

2. Run the failing test with `rust-gdb`.

```shell
rust-gdb /vagrant/target/debug/deps/libzfs-37d0dad38d98d030
```

Then set any breakpoints and run the tests:

```shell
b lib.rs:533
run --test
```

When running you may notice some missing debuginfos in the output. You can copy paste the suggested command to install them and try debugging again.

