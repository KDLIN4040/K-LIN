define( function( require ) {
  'use strict';

  // Module globals
  var ws, scene, camera, renderer, controls, box;

  init();
  animate();

  function init() {

    var coords = require( 'Coordinates' );
    THREE.TrackballControls = require( 'TrackballControls' );

    // SCENE
    scene = new THREE.Scene();

    // RENDERER
    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth/3, window.innerHeight/3 );
    document.body.appendChild( renderer.domElement );

    // BOX (IMU CHIP)
    var boxGeom = new THREE.BoxGeometry( 2, 2, 0.5 ); // width, height, depth
    var boxMaterial = new THREE.MeshLambertMaterial( {
      color: 0x7f7f7f
    } );
    box = new THREE.Mesh( boxGeom, boxMaterial );
    box.position.set( 1, 1, 1 );

    // CAMERA
    camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
    camera.position.set( box.position.x, box.position.y-3, box.position.z+3 );
    camera.lookAt( box.position.x, box.position.y, box.position.z );
    scene.add( box );

    // DOT MARKER
    var dotGeom = new THREE.CircleGeometry( 0.25, 32 );
    var dotMaterial = new THREE.MeshLambertMaterial( {
      color: 0xffffff
    } );
    var dot = new THREE.Mesh( dotGeom, dotMaterial );
    dot.position.set(
      boxGeom.parameters.width / 2 - 0.4,
      boxGeom.parameters.height / 2 - 0.4,
      boxGeom.parameters.depth / 2 + 0.01 );
    box.add( dot );

    // 'BN0 055' TEXT LABEL
    var fontLoader = new THREE.FontLoader();
    fontLoader.load( 'static/js/lib/helvetiker_regular.typeface.js', function( response ) {
      var textMaterial = new THREE.MeshPhongMaterial( {
        color: 0xdddddd
      } );
      var textGeom = new THREE.TextGeometry( '--IMU--', {
        font: response,
        size: 0.3,
        height: 0.01,
        curveSegments: 4,
        bevelThickness: 0.005,
        bevelSize: 0.005,
        bevelEnabled: true
      } );
      var textMesh = new THREE.Mesh( textGeom, textMaterial );
      textMesh.position.set( -0.5, 0.8, boxGeom.parameters.depth / 2 + 0.001 );
      textMesh.rotation.set( 0, 0, -Math.PI / 2 );

      box.add( textMesh );
      render();
    } );

    // HORIZONTAL GRID
    scene.add( coords.grid( {
      size: 8,
      scale: 1,
      orientation: 'z'
    } ) );

    // AXES
    var localAxes = coords.axes( {
      axisLength: 3,
      axisRadius: 0.02,
      axisTess: 50
    } );
    localAxes.forEach( function( item ) {
      box.add( item );
    } );
    var axes = coords.axes( {
      axisLength: 5,
      axisRadius: 0.05,
      axisTess: 50
    } );
    axes.forEach( function( item ) {
      scene.add( item );
    } );

    // CAMERA TRACKBALL CONTROLS
    addControls();

    // LIGHTING
    scene.add( new THREE.AmbientLight( 0x444444 ) );
    var pointLight = new THREE.PointLight( 0xFFFFFF );
    pointLight.position.set( 5, 5, 10 );
    scene.add( pointLight );

    render();
  }

  // Camera position controller
  function addControls() {
    controls = new THREE.TrackballControls( camera );
    // controls.target.set( 0, 0, 0 );
    controls.target.set( box.position.x, box.position.y, box.position.z );
    controls.rotateSpeed = 1.0;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;
    controls.noZoom = false;
    controls.noPan = false;
    controls.staticMoving = true;
    controls.dynamicDampingFactor = 0.3;
    controls.keys = [ 65, 83, 68 ];
    controls.addEventListener( 'change', render );
    controls.update();
  }
  

  function animate() {
    requestAnimationFrame( animate );
    controls.update();
  }
  function render() {
    renderer.render( scene, camera );
  }

  // Update box orientation from websocket message data
  function updateBox( roll,pitch,yaw ) {
    roll *= (Math.PI/180);
    pitch *= (Math.PI/180);
    yaw *= (Math.PI/180);
    var angle = new THREE.Euler(roll,pitch,yaw);
    box.rotation.set( roll,pitch,yaw );
    render();
  }
  var t1 = setInterval(function(){
    imu();
  },1000);

  function imu(){
    $.ajax({
    url:'http://192.168.43.190:81/getattitude',
    type:'get',
    cache:false,
    success:function(response){
      var response = response.split(",", 3);
      console.log(response[0]);
      console.log(response[1]);
      console.log(response[2]);
      updateBox(response[0],response[1],response[2]);

    }
    }) 
}

} );
