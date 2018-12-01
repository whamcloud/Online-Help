<a id="13.0"></a>
# Glossary

[**Online Help Table of Contents**](IML_Help_TOC.md)

**chroma-agent.** An executable provided with the Integrated Manager for Lustre software that can be installed as a service on Lustre servers to enable monitoring of Lustre file systems not created by the Integrated Manager for Lustre software. 

**Lustre clients.** Lustre clients are computational, visualization, or desktop nodes that are running Lustre client software, allowing them to mount the Lustre file system.

**Management target (MGT).** The MGT stores configuration information for all the Lustre file systems in a cluster and provides this information to other Lustre components. Each Lustre object storage target (OST) contacts the MGT to provide information, and Lustre clients contact the MGT to retrieve information.

**Metadata target (MDT).** Each Lustre file system has one MDT. The MDT stores metadata (such as file names, directories, permissions, and file layout) for attached storage and makes them available to clients.

**Object storage target (OST).** User file data is stored in one or more objects that are located on separate OSTs in the Lustre file system. The number of objects per file is configurable by the user and can be tuned to optimize performance for a given workload.

**Storage server.** A server on which an MGT, MDT, or OST is located. 

**Target.** See metadata target, management target, object storage target.

**Volumes.** (also called LUNs or block devices) are the underlying units of storage used to create Lustre file systems. Each Lustre target corresponds to a single volume. If servers in the volume have been configured for high availability, primary and failover servers can be designated for a Lustre target. Only volumes that are not already in use as Lustre targets or local file systems are shown. A volume may be accessible on one or more servers via different device nodes, and it may be accessible via multiple device nodes on the same host.


[Top of page](#13.0)