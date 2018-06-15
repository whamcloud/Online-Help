# <a name="1.0"></a>Getting Help

[**Software Installation Guide Table of Contents**](ig_TOC.md)

*For partners*: If you encounter a problem with Integrated Manager for Lustre* software or storage, and you
require support from your technical support representative, then
to help expedite resolution of the problem, please do the following:

1.  [Run iml diagnostics](#run-iml-diagnostics).

2.  [Submit a ticket](#submit-a-ticket).

Run iml diagnostics
----------------------

Run iml-diagnostics on any of the servers that you suspect may be
having problems, and on the server hosting the Integrated Manager for Lustre*
software dashboard. Iml-Diagnostics generates a compressed
tar.xz file that you should attach to your GitHub issue.
To run iml-diagnostics:

1.  Log into the server in question as Admin. Admin login is required in
    order to collect all desired data.

2.  Enter the following command at the prompt:

    ```
    # iml-diagnostics
    ```

    The following results are displayed after running this command. (The resulting tar.xz file will have a different file name.)

    ```
    sosreport (version 3.4)

    This command will collect diagnostic and configuration information from
    this CentOS Linux system and installed applications.

    An archive containing the collected information will be generated in
    /var/tmp/sos.p3Djuo and may be provided to a CentOS support
    representative.

    Any information provided to CentOS will be treated in accordance with
    the published support policies at:

    https://wiki.centos.org/

    The generated archive may contain data considered sensitive and its
    content should be reviewed by the originating organization before being
    passed to any third party.

    No changes will be made to system configuration.


    Setting up archive ...
    Setting up plugins ...
    Running plugins. Please wait ...

    Running 1/10: block...
    Running 2/10: filesys...
    Running 3/10: iml...
    Running 4/10: kernel...
    Running 5/10: logs...
    Running 6/10: memory...
    Running 7/10: pacemaker...
    Running 8/10: pci...
    Running 9/10: processor...
    Running 10/10: yum...

    Creating compressed archive...

    Your sosreport has been generated and saved in:
    /var/tmp/sosreport-iml.dev-20171017003954.tar.xz

    The checksum is: f018ba301df835862e559aa98465e9fc

    Please send this file to your support representative.
    ```


1.  You can also decompress the file and examine the results. To unpack
    and extract the files, use this command:

    ```
    # tar --xz -xvpf <file_name>.tar.xz
    ```


1.  If desired, the following command returns help for chroma
    diagnostics:

    ```
    # iml-diagnostics -h
    ```


Submit a ticket
---------------

You can submit a ticket using the GitHub issue tracking system. Attach the
sos report to the ticket.

1.  Look through existing issues to see if any relevant answers exist:
    <https://github.com/intel-hpdd/intel-manager-for-lustre/issues>

2.  If still required, log in to the GitHub issue tracker at:
    <https://github.com/intel-hpdd/intel-manager-for-lustre/issues/new>

3.  Fill in the issue details, paying attention to the suggested template.

4.  Click "Submit new issue" and await a response.

[Top of page](#1.0)
