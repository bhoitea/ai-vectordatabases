### **2. `scripts/run_yugabyte.sh`**
#!/bin/bash
set -e

docker pull yugabytedb/yugabyte:2.25.2.0-b359

docker run -d --name yugabyte -p 7000:7000 -p 9000:9000 -p 15433:15433 -p 5433:5433 -p 9042:9042 \
yugabytedb/yugabyte:2.25.2.0-b359 bin/yugabyted start \
--background=false

echo "YugabyteDB is running"



---


