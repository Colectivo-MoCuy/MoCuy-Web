
document.addEventListener('DOMContentLoaded', function(){
  const data = window.DOSSIER_DATA || {};
  const presupuesto = data.presupuesto || {};
  const total = data.total_general || 0;

  const labels = Object.keys(presupuesto);
  const values = labels.map(l => presupuesto[l]);

  const pieData = [{ type:'pie', labels: labels, values: values, textinfo:'label+percent', hoverinfo:'label+value', marker:{line:{color:'#0f1724',width:1}} }];
  const pieLayout = { margin:{t:10,b:10,l:10,r:10}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', legend:{font:{color:'#EAE8F9'}} };
  Plotly.newPlot('chart_presupuesto', pieData, pieLayout, {responsive:true});

  const aLabels = Object.keys(data.alcance || {});
  const aValues = aLabels.map(k => data.alcance[k]);
  const alcData = [{ type:'pie', labels:aLabels, values:aValues, textinfo:'label+percent' }];
  const alcLayout = { margin:{t:10,b:10,l:10,r:10} };
  Plotly.newPlot('chart_alcance', alcData, alcLayout, {responsive:true});
});
