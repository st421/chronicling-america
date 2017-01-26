function addPies(path, map_elements, pies, election) {
  var g = pies.selectAll(".pie").data(map_elements.features.filter(function(d) { return isMentioned(d, election.candidates); }))
    .enter().append("svg").attr("class","pie").each(addPie).select("g");
      
  function addPie(d) {
    var pie = d3.layout.pie().sort(null).value(function(c) { return getMentions(d, c.mentions); });
    var r = radius(totalMentions(d,election.candidates), election.max);
    var diam = 2*r;
    var arc = d3.svg.arc().outerRadius(r).innerRadius(r*0.4); 
    
    var pie_svg = d3.select(this).attr("width", diam).attr("height", diam)
      .append("g").attr("transform", "translate("+path.centroid(d)+")");
    pie_svg.append("circle").attr("r",r).attr("class",pie_class(d, election.candidates));
    pie_svg.selectAll(".arc").data(pie(election.candidates)).enter()
      .append("a").attr("xlink:href", function(c) { return timelineLink(election.year, c.data.last, d); }).attr("class", function(c) { return arc_class(c.data); })
      .append("path").attr("d", arc)
      .append("title").text(function(c) { return d.properties.name + " | " + c.data.last + " | " + getMentions(d, c.data.mentions) + " front pages--click for timeline"; });
  }
}

function isMentioned(us_element, candidates) {
  for(var i = 0; i < candidates.length; i++) {
    var c = candidates[i];
    if(us_element.id in c.mentions) return true;
  }
  return false;
}
  
function timelineLink(year, last_name, element) {
  return "getTimelinePath/".concat(year).concat("/").concat(last_name).concat("/").concat(element.id);
}
  
function totalMentions(us_element, candidates) {
  var total = 0;
  for(var i=0; i < candidates.length; i++) {
    total += getMentions(us_element, candidates[i].mentions);
  }
  return total;
}
  
function getMentions(us_element, mentions) {
  if(us_element.id in mentions) {
    return mentions[us_element.id];
  } else {
    return 0;
  }
}
  
function radius(r, max) {
  var rad = d3.scale.sqrt().domain([0, max]).range([10, 30]);
  return rad(r);
}

function arc_class(c) {
  return "arc fill-"+c.color;
}
  
function pie_class(el, cs) {
  for(var i=0; i < cs.length; i++) {
    var c = cs[i];
    if(c.won.includes(el.properties.abbrev)) {
      return "state-w-" + c.color;
    }
  }
  return "state-w-purple";
}

function us_element_class(us_element, year) {
  var class_name, admit = us_element.properties.admit; 
  if(admit != 0 && admit <= year) {
    class_name = "state";
  } else {
    class_name = "territory";
  }
  return class_name;
}