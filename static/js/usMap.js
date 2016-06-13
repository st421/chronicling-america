function us_map() {
  var width = 720, // default width
      height = 80; // default height

  function my() {
    // generate chart here, using `width` and `height`
  }

  my.width = function(value) {
    if (!arguments.length) return width;
    width = value;
    return my;
  };

  my.height = function(value) {
    if (!arguments.length) return height;
    height = value;
    return my;
  };

  return my;
  
  
    var year = {{e.year}};
  console.log(year);
  var svgStates = d3.select("svg #states");
  //var width = window.innerWidth,height = window.innerHeight;
  var projection = d3.geo.albersUsa().scale(1100);
  var path = d3.geo.path().projection(projection);
  var us_map = loadJson("{{e.getMapPath()}}");
  var us_elements = topojson.feature(us_map, us_map.objects.stdin);
  drawMap(us_elements);
  addStats(loadJson("{{e.getStatsPath()}}"));
  
  function loadJson(path) {
    d3.json(path, function(error, items) {
      if (error) return console.error(error);
      return items;
    });
  }

  function drawMap(us_elements) {
    svgStates.selectAll("path").data(us_elements.features).enter().append("path").attr("d", path).attr("class",function(d) { return isState(d); });
  }
  
  function addStats(stats) {
    var max = stats[0].mentions.max;
    for(i=0; i<stats.length; i++) {
      stat = stats[i];
      if(stat.mentions.max > max) max = stat.mentions.max;
    }
    {% for candidate in e.candidates %}
    for(i=0; i<stats.length; i++) {
      if(stats[i].candidate == "{{candidate.last}}") {
        stat = stats[i];
        addBubbles(stat.candidate, stat.mentions, "{{candidate.color}}", max, i);
      }
    }
    {% endfor %}
  }
  
  function addBubbles(c, m, color, max, i) {
    svgStates.append("g").selectAll("a")
      .data(us_elements.features).enter().append("a")
      .attr("xlink:href", function(d) { var path = "getTimelinePath/".concat(year).concat("/").concat(c).concat("/").concat(d.properties.name); return path;})
      .append("circle")
      .attr("transform", function(d) { return "translate(" + adjustCenter(path.centroid(d), i, getRadius(d, m, max)) + ")"; })
      .attr("r", function(d) { return getRadius(d, m, max); })
      .attr("class",color)
      .append("title").text(function(d) { return "See " + d.properties.name + " coverage of " + c;});
  }
  
  function adjustCenter(c, i, amt) {
    if(i == 0) {
      return [c[0],c[1] - amt];
    } else {
      return [c[0],c[1] + amt];
    }
  }
  
  function getRadius(us_element, data_set, max) {
    var radius = d3.scale.sqrt().domain([0, max]).range([5, 20]);
    if(data_set.hasOwnProperty(us_element.id)) {
      return radius(data_set[us_element.id]);
    } else {
      return 0;
    }
  }
  
  function isState(us_element) {
    var class_name, admit = us_element.properties.admit; 
    if(admit != 0 && admit <= year) {
      class_name = "state";
    } else {
      class_name = "territory";
    }
    return class_name;
  }
  
  function getPartyColor(party) {
    var red = "red";
    var blue = "blue"; 
    
    var party_colors = {
        "Democratic":blue,
        "Whig":red,
        "Republican":red,
        "Progressive":red
    }
    return party_colors[party];
  }
}