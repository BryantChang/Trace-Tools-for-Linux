#!/bin/bash
function usage {
    echo "usage:autorun <test/pic> <ftrace log location> <cmd> <the output path>"
    exit
}

#判断参数个数是否合法
if [ $# -lt 4 ]
then
    usage
fi

base_dir=$(dirname $2)

tmp_file_name="ftrace_"${3}"_tmp.log"
tmp_file_loc=${base_dir}"/"${tmp_file_name}
echo "generate the log of you cmd "${3}"..."
cat $2 | grep $3 > $tmp_file_loc
echo "generate completed!!"

echo "generate the file to be handled..."
py_input_log_name="ftrace_"${3}"_res.log"
py_input_log_loc=${base_dir}"/"${py_input_log_name}
`awk '{print \$5,\$6,\$7}' ${tmp_file_loc} > ${py_input_log_loc}`
echo "generate completed"
echo "remove the tmp log"
rm -rf $tmp_file_loc

echo "check the config file of python script..."
config_loc="./config"
if [ -e $config_loc ]
then
    echo "file exists remove it first"
    rm -rf $config_loc
fi
echo "setting the config file of python..."

echo "setting mode..."
echo "mode="${1} >> $config_loc

echo "setting ftrace log path..."
echo "ftrace_log_path="${py_input_log_loc} >> $config_loc

echo "setting output path..."
if [ $1 = "text" ]
then
    echo "output_text_log_path="${4} >> $config_loc

elif [ $1 = "pic" ]
then
    mkdir -p ${4}
    echo "output_pic_log_dir="${4} >> $config_loc
fi
echo "set completed..."

echo "analysing the log..."
cmd="python log_analyzer.py "${config_loc}
`$cmd`
echo "analysis completed..."
#rm -rf ${py_input_log_loc}
if [ $1 = "text" ]
then
    echo "all completed,now exit"
    exit

elif [ $1 = "pic" ]
then
    if [ $# -eq 4 ]
    then
        echo "The count of file is too large,please generate the gif by your self,now target the dot file."
        res_tar=${base_dir}"/dot.tar.gz"
        echo "generate the tar file."
        echo ${res_tar}
        tar -czf ${res_tar} ${4}*
        echo "generate completed now exit"
        rm -rf ${4}
        exit
    elif [ $# -eq 5 ]
    then
        echo "filtering files by function name"
        filter_dir=${base_dir}"/"${5}"_dot_dir"
        tar_dir=${base_dir}"/"${5}"_pic.tar.gz"
        mkdir -p $filter_dir
        cd ${4}
        file_list=`ls`
        for file in $file_list
        do
            `grep -q "${5}" "${file}" && cp "${file}"  "${filter_dir}"`
            #file_name=${file#*.}
            #dot -Tgif ${file} -o ../${5}_pic_dir/${file_name}.gif   
        done
        echo "filter completed!!"
        echo "generating the gif file...."
        cd ${filter_dir}
        file_list_filter=`ls`
        res_gif_dir=${base_dir}"/"${5}"_pic_dir"
        mkdir -p $res_gif_dir
        for file_filter in $file_list_filter
        do
	    file_name=${file_filter%\.*}
            dot -Tgif ${file_filter} -o ${res_gif_dir}/${file_name}.gif 2>/dev/null
        done
        cd ../
        echo "generate completed!! now remove the dot dir"
        rm -rf ${4}
        rm -rf ${filter_dir}
        echo "now target the file"
        tar -czf ${tar_dir}  ${res_gif_dir}* 2>/dev/null
        echo "all completed!!" 
    fi    
fi


