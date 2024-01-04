LOG=$1

echo "平均值:"
cat $LOG | awk '{sum += $3} END {avg = sum / NR; print avg}'
echo ""

echo "最小值:"
cat $LOG | awk '{print $3}' | sort -n | head -n 1
echo ""

echo "最大值:"
cat $LOG | awk '{print $3}' | sort -n | tail -n 1
echo ""

echo "90分位:"
cat $LOG | awk '{print $3}' | sort -n | awk 'BEGIN{count=0} {arr[count++]=$1} END{print arr[int(NR*0.9)]}'
echo ""

# 感知 alog cost 统计
echo "最小值:"
cat krider_multiperception_car.INFO |grep Algo |grep cost | awk '{print $9}'|sort -n |head -n 1

echo "最大值:"
cat krider_multiperception_car.INFO |grep Algo |grep cost | awk '{print $9}'|sort -n |tail -n 1

echo "平均值:"
cat krider_multiperception_car.INFO |grep Algo |grep cost | awk '{sum += $9} END {avg = sum / NR; print avg}'

# 感知 alog fps 统计
echo "最小值:"
cat krider_multiperception_car.INFO |grep Algo |grep fps | awk '{print $10}'|sort -n |head -n 1

echo "最大值:"
cat krider_multiperception_car.INFO |grep Algo |grep fps | awk '{print $10}'|sort -n |tail -n 1

echo "平均值:"
cat krider_multiperception_car.INFO |grep Algo |grep fps | awk '{sum += $10} END {avg = sum / NR; print avg}'