# 全局 remote debug
export JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

用完后注意
unset JAVA_TOOL_OPTIONS

F7 会进入JAR包代码， F5只进入你自己的代码