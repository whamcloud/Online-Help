# Getting Help

[**Software Installation Guide Table of Contents**](ig_TOC.md)

_For partners_: If you encounter a problem with Integrated Manager for Lustre software or storage, and you
require support from your technical support representative, then
to help expedite resolution of the problem, please do the following:

1. [Run sosreport](#run-sosreport).

1. [Submit a ticket](#submit-a-ticket).

## Run sosreport

Run `sosreport` on any of the servers that you suspect may be
having problems, and on the server hosting the Integrated Manager for Lustre
software dashboard. `sosreport` generates a compressed
`tar.xz` file that you should attach to your GitHub issue.
To run `sosreport`:

1. Log into the server in question as root. root login is required in
   order to collect all desired data.

1. Enter the following command at the prompt:

   ```sh
   # sosreport
   ```

   The following results are displayed after running this command. (The resulting tar.xz file will have a different file name.)

   ```text
    sosreport (version 3.6)

    This command will collect diagnostic and configuration information from
    this CentOS Linux system and installed applications.

    An archive containing the collected information will be generated in
    /var/tmp/sos.myCg1i and may be provided to a CentOS support
    representative.

    Any information provided to CentOS will be treated in accordance with
    the published support policies at:

    https://wiki.centos.org/

    The generated archive may contain data considered sensitive and its
    content should be reviewed by the originating organization before being
    passed to any third party.

    No changes will be made to system configuration.

    Press ENTER to continue, or CTRL-C to quit.

    Please enter the case id that you are generating this report for []:

    Setting up archive ...
    Setting up plugins ...
    Running plugins. Please wait ...

    Finishing plugins              [Running: yum]
    Finished running plugins
    Creating compressed archive...

    Your sosreport has been generated and saved in:
    /var/tmp/sosreport-mds1-2019-04-23-lekbjdv.tar.xz

    The checksum is: f074e8c8250c2e6b682aa975ca985eb8

    Please send this file to your support representative.
   ```

1. You can also decompress the file and examine the results. To unpack
   and extract the files, use this command:

   ```sh
   # tar --xz -xvpf <file_name>.tar.xz
   ```

1. If desired, the following command returns help for `sosreport`:

   ```sh
   # sosreport -h
   ```

## Submit a ticket

You can submit a ticket using the GitHub issue tracking system. Attach the
sos report to the ticket.

1. Look through existing issues to see if any relevant answers exist:
   <https://github.com/whamcloud/integrated-manager-for-lustre/issues>

1. If still required, log in to the GitHub issue tracker at:
   <https://github.com/whamcloud/integrated-manager-for-lustre/issues/new>

1. Fill in the issue details, paying attention to the suggested template.

1. Click "Submit new issue" and await a response.

[Top of page](#getting-help)
