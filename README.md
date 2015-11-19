#Trace-Tools
<h3>This is a collect of trace tools of OS,including ltrace and ftrace,and it can also analyze the ftrace log automatically</h3>
<h4>usage of these tools</h4>
<b>1 trace(a shell script)</b><br/>
<b>The function of this tool is collect the ltrace and ftrace</b></br>
<li>use ltrace including the system call:</br>
./trace ltrace normal system (the log path) (cmd)</li>
<li>use ltrace not including the system call:<br/>
./trace ltrace normal li (the log path) (cmd)</li>
<li>use ltrace including the system call(time):</br>
./trace ltrace time system (the log path) (cmd)</li>
<li>use ltrace not including the system call(time):<br/>
./trace ltrace time li (the log path) (cmd)</li>
<li>use ftrace</li>
./trace ftrace (the path that debugfs mount) (tracer function/function\_graph) (the path of output logs) (cmd of your program)</br>
<b>2 autorun.sh(a shell script)</b><br/>
<b>The function of this tool is to analyze the log of ftrace and generate the function graph of the function of kernel</b><br/>
<b>The usage of this tool is</b><br/>
./autorun.sh (the format of final log pic/text) (path of ftrace log) (cmd of your process) (path of output log) (kernel function name)
