for i in dat/*.zip; do
  quakeio -St yaml $i > /dev/null
  quakeio -t  yaml $i > /dev/null
done

