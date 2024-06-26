/**
* Template Name: NiceAdmin
* Template URL: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/
* Updated: Mar 17 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */
  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

  tinymce.init({
    selector: 'textarea.tinymce-editor',
    plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons',
    editimage_cors_hosts: ['picsum.photos'],
    menubar: 'file edit view insert format tools table help',
    toolbar: 'undo redo | bold italic underline strikethrough | fontfamily fontsize blocks | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
    toolbar_sticky: true,
    toolbar_sticky_offset: isSmallScreen ? 102 : 108,
    autosave_ask_before_unload: true,
    autosave_interval: '30s',
    autosave_prefix: '{path}{query}-{id}-',
    autosave_restore_when_empty: false,
    autosave_retention: '2m',
    image_advtab: true,
    link_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_class_list: [{
        title: 'None',
        value: ''
      },
      {
        title: 'Some class',
        value: 'class-name'
      }
    ],
    importcss_append: true,
    file_picker_callback: (callback, value, meta) => {
      /* Provide file and text for the link dialog */
      if (meta.filetype === 'file') {
        callback('https://www.google.com/logos/google.jpg', {
          text: 'My text'
        });
      }

      /* Provide image and alt text for the image dialog */
      if (meta.filetype === 'image') {
        callback('https://www.google.com/logos/google.jpg', {
          alt: 'My alt text'
        });
      }

      /* Provide alternative source and posted for the media dialog */
      if (meta.filetype === 'media') {
        callback('movie.mp4', {
          source2: 'alt.ogg',
          poster: 'https://www.google.com/logos/google.jpg'
        });
      }
    },
    templates: [{
        title: 'New Table',
        description: 'creates a new table',
        content: '<div class="mceTmpl"><table width="98%%"  border="0" cellspacing="0" cellpadding="0"><tr><th scope="col"> </th><th scope="col"> </th></tr><tr><td> </td><td> </td></tr></table></div>'
      },
      {
        title: 'Starting my story',
        description: 'A cure for writers block',
        content: 'Once upon a time...'
      },
      {
        title: 'New list with dates',
        description: 'New List with dates',
        content: '<div class="mceTmpl"><span class="cdate">cdate</span><br><span class="mdate">mdate</span><h2>My List</h2><ul><li></li><li></li></ul></div>'
      }
    ],
    template_cdate_format: '[Date Created (CDATE): %m/%d/%Y : %H:%M:%S]',
    template_mdate_format: '[Date Modified (MDATE): %m/%d/%Y : %H:%M:%S]',
    height: 600,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    contextmenu: 'link image table',
    skin: useDarkMode ? 'oxide-dark' : 'oxide',
    content_css: useDarkMode ? 'dark' : 'default',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
  });

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ["All", -1]],
      columns: [{
          select: 2,
          sortSequence: ["desc", "asc"]
        },
        {
          select: 3,
          sortSequence: ["desc"]
        },
        {
          select: 4,
          cellClass: "green",
          headerClass: "red"
        }
      ]
    });
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

})();


// Total Cars
// google.charts.load('current', {packages: ['corechart', 'bar']});
// google.charts.setOnLoadCallback(drawBasic1);

// function drawBasic1() {

//       var data = new google.visualization.DataTable();
//       data.addColumn('timeofday', 'Time of Day');
//       data.addColumn('number', 'Motivation Level');

//       data.addRows([
//         [{v: [8, 0, 0], f: '8 am'}, 1],
//         [{v: [9, 0, 0], f: '9 am'}, 2],
//         [{v: [10, 0, 0], f:'10 am'}, 3],
//         [{v: [11, 0, 0], f: '11 am'}, 4],
//         [{v: [12, 0, 0], f: '12 pm'}, 5],
//         [{v: [13, 0, 0], f: '1 pm'}, 6],
//         [{v: [14, 0, 0], f: '2 pm'}, 7],
//         [{v: [15, 0, 0], f: '3 pm'}, 8],
//         [{v: [16, 0, 0], f: '4 pm'}, 9],
//         [{v: [17, 0, 0], f: '5 pm'}, 10],
//       ]);

//       var options = {
//         title: 'Motivation Level Throughout the Day',
//         height: 400,
//         hAxis: {
//           title: 'Time of Day',
//           format: 'h:mm a',
//           viewWindow: {
//             min: [7, 30, 0],
//             max: [17, 30, 0]
//           },
//         },
//         vAxis: {
//           title: 'Rating (scale of 1-10)'
//         }
//       };

      // var chart = new google.visualization.ColumnChart(
      //   document.getElementById('chart_div1'));

      // chart.draw(data, options);
//     }


/* ******************************************************** */
// Count of Speeding vs Highway
/* ******************************************************** */
google.charts.load('current', {packages: ['corechart', 'bar']});
// google.charts.setOnLoadCallback(drawBasic2);

// function drawBasic2() {
//   var data = google.visualization.arrayToDataTable([
//     ['City', '2010 Population',],
//     ['New York City, NY', 8175000],
//     ['Los Angeles, CA', 3792000],
//     ['Chicago, IL', 2695000],
//     ['Houston, TX', 2099000],
//     ['Philadelphia, PA', 1526000]
//   ]);

//   var options = {
//     title: 'Population of Largest U.S. Cities',
//     chartArea: {width: '50%'},
//     height: 270,
//     hAxis: {
//       title: 'Total Population',
//       minValue: 0
//     },
//     vAxis: {
//       title: 'City'
//     }
//   };

//   var chart = new google.visualization.BarChart(document.getElementById('chart_div2'));

//   chart.draw(data, options);
// }



/* ******************************************************** */
/* Google Charts */
/* ******************************************************** */
// google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(drawChart1);
// google.charts.setOnLoadCallback(drawChart2);

// function drawChart1() {
//   var data = google.visualization.arrayToDataTable([
    // ['Task', 'Hours per Day'],
    // ['Work',     11],
    // ['Eat',      2],
    // ['Commute',  2],
    // ['Watch TV', 2],
    // ['Sleep',    7]
//   ]);

//   var options = {
//     // title: 'Accidents',
//     // fontSize: 10,
//     // width: 300,
//     // height: 300,
//     chartArea: {'width': '100%', 'height': '100%'},
//     // legend: {'position': 'right'}
//     legend: {'position': 'none'}
//   };

//   var chart = new google.visualization.PieChart(document.getElementById('piechart1'));

//   chart.draw(data, options);
// }

// function drawChart2() {
//   var data = google.visualization.arrayToDataTable([
//     ['Status', 'Numbers'],
//     ['Online',     60],
//     ['Offline',      40]
//   ]);

//   var options = {
//     // title: 'Accidents',
//     // fontSize: 10,
//     // width: 300,
//     // height: 300,
//     chartArea: {'width': '100%', 'height': '100%'},
//     legend: {'position': 'none'}
//   };

//   var chart = new google.visualization.PieChart(document.getElementById('piechart2'));

//   chart.draw(data, options);
// }



/* ******************************************************** */
/* Google Table */
/* ******************************************************** */
google.charts.load('current', {'packages':['table']});
// google.charts.setOnLoadCallback(drawTable);

// function drawTable() {
//   var data = new google.visualization.DataTable();
//   data.addColumn('string', 'Area');
//   data.addColumn('number', 'In');
//   data.addColumn('number', 'Out');
//   data.addColumn('number', 'Volumes');
//   data.addRows([
//     ['Area-1',  30, 50, 80],
//     ['Area-2',  40, 40, 80],
//     ['Area-3',  50, 30, 80],
//     ['Area-4',  60, 20, 80],
//     ['Area-5',  70, 10, 80],
//     ['Area-5',  70, 10, 80],
//     ['Area-5',  70, 10, 80],
//     // ['Area',   {v: 7000,  f: '$7,000'},  true]
//   ]);

//   var table = new google.visualization.Table(document.getElementById('table_div'));

//   table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
// }


// google.charts.load('current', {'packages':['table']});
// google.charts.setOnLoadCallback(drawTable2);

// function drawTable2() {
//   var data = new google.visualization.DataTable();
//   data.addColumn('number', 'RecordID');
//   data.addColumn('number', 'id');
//   data.addColumn('string', 'Date');
//   data.addColumn('string', 'Data Sorce');
//   data.addColumn('string', 'Location');
//   data.addColumn('string', 'Licence Plate');
//   data.addColumn('string', 'Brand');

//   data.addColumn('string', 'Car Type');
//   data.addColumn('string', 'Color');
//   data.addColumn('number', 'Speed Limit');
//   data.addColumn('number', 'Speed');
//   data.addColumn('number', 'Exceeding Rate');
//   data.addColumn('string', 'Video');
//   data.addColumn('string', 'Image');
//   data.addColumn('string', 'Status');
//   data.addColumn('string', 'Detail');
//   data.addRows([
//     [1, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//     [2, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//     [3, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//     [4, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//     [5, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//     [6, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//     [7, "1/1/2024 10:00:00", "Camera", "Highway-1", "AAA001", "Toyota", "Compact", "White", 100, 100, 0, "Link", "Link", "Reported", "-"],
//   ]);

//   var table = new google.visualization.Table(document.getElementById('table_div2'));

//   table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
// }


// google.charts.load('current', {'packages':['table']});
// google.charts.setOnLoadCallback(drawTable3);

// function drawTable3() {
//   var data = new google.visualization.DataTable();
//   data.addColumn('string', 'Area');
//   data.addColumn('number', 'In');
//   data.addColumn('number', 'Out');
//   data.addColumn('number', 'Volumes');
//   data.addRows([
//     ['Area-1',  30, 50, 80],
//     ['Area-2',  40, 40, 80],
//     ['Area-3',  50, 30, 80],
//     ['Area-4',  60, 20, 80],
//     ['Area-5',  70, 10, 80],
//     ['Area-5',  70, 10, 80],
//     ['Area-5',  70, 10, 80],
//     // ['Area',   {v: 7000,  f: '$7,000'},  true]
//   ]);

//   var table = new google.visualization.Table(document.getElementById('table_div3'));

//   table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
// }


// google.charts.load('current', {'packages':['table']});
// google.charts.setOnLoadCallback(drawTable4);

// function drawTable4() {
//   var data = new google.visualization.DataTable();
//   data.addColumn('string', 'Area');
//   data.addColumn('number', 'In');
//   data.addColumn('number', 'Out');
//   data.addColumn('number', 'Volumes');
//   data.addRows([
//     ['Area-1',  30, 50, 80],
//     ['Area-2',  40, 40, 80],
//     ['Area-3',  50, 30, 80],
//     ['Area-4',  60, 20, 80],
//     ['Area-5',  70, 10, 80],
//     ['Area-5',  70, 10, 80],
//     ['Area-5',  70, 10, 80],
//     // ['Area',   {v: 7000,  f: '$7,000'},  true]
//   ]);

//   var table = new google.visualization.Table(document.getElementById('table_div4'));

//   table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
// }


let dropArea = document.getElementById('drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false);
  document.body.addEventListener(eventName, preventDefaults, false);
});

['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight(e) {
  dropArea.classList.add('highlight');
}

function unhighlight(e) {
  dropArea.classList.remove('highlight');
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
  let dt = e.dataTransfer;
  let files = dt.files;
  handleFiles(files);
}

function handleFiles(files) {
  ([...files]).forEach(uploadFile);
}

function uploadFile(file) {
  // let url = 'YOUR_UPLOAD_ENDPOINT'; // Change this to your upload processing endpoint
  let formData = new FormData();
  formData.append('file', file);
  
  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(() => { /* Handle success */ })
  .catch(() => { /* Handle error */ });
}






////////////////////////////////////////////////////////////////
// Google map
////////////////////////////////////////////////////////////////
// let map;

// function initMap() {
//   const mapOptions = {
//     zoom: 8,
//     center: { lat: -34.397, lng: 150.644 },
//   };

//   map = new google.maps.Map(document.getElementById("map"), mapOptions);

//   const marker = new google.maps.Marker({
//     // The below line is equivalent to writing:
//     // position: new google.maps.LatLng(-34.397, 150.644)
//     position: { lat: -34.397, lng: 150.644 },
//     map: map,
//   });

//   const infowindow = new google.maps.InfoWindow({
//     content: "<p>Marker Location:" + marker.getPosition() + "</p>",
//   });

//   google.maps.event.addListener(marker, "click", () => {
//     infowindow.open(map, marker);
//   });
// }

// window.initMap = initMap;
