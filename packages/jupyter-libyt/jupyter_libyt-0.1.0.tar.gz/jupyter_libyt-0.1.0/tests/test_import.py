def test_import():
    import jupyter_libyt.provisioning

    assert hasattr(
        jupyter_libyt.provisioning, "LibytKernelProvisioner"
    ), "Cannot find LibytKernelProvisioner"
