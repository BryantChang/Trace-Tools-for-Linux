#Trace-Tools
<h3>This is a collect of trace tools of OS,including ltrace and ftrace and it can also analyze the ftrace log automatically</h3>
<h4>usage of these tools</h4>
<b>1 trace(a shell script)</b><br/>
<li>use ltrace including the system call:</br>
./trace ltrace normal system <the log path> <cmd></li>
<li>use ltrace not including the system call:<br/>
./trace ltrace normal li <the log path> <cmd></li>
<li>use ltrace including the system call(time):</br>
./trace ltrace time system <the log path> <cmd></li>
<li>use ltrace not including the system call(time):<br/>
./trace ltrace time li <the log path> <cmd></li>
