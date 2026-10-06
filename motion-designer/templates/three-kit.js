// three-kit.js — reusable 3D recipes for motion videos (Three.js r170 vendored in <skill>/lib/three).
// Everything is a pure function of t (deterministic): build objects once, then set their state in seek(t).
//
// In timeline.html (module script + import map — paths are absolute file:// so renders work offline):
//   <script type="importmap">{"imports":{"three":"file:///ABS/SKILL/lib/three/build/three.module.js",
//                                        "three/addons/":"file:///ABS/SKILL/lib/three/examples/jsm/"}}</script>
//   <script type="module"> import * as K from 'file:///ABS/SKILL/templates/three-kit.js'; ... </script>
// render.py launches Chromium with Metal GPU + --allow-file-access-from-files (~20 ms/frame). fetch() of file:// is
// blocked even with that flag — that's why every loader below goes through XHR + parse().
//
//   const G = await K.init3D(stage, W, H, {bloom:true});           // renderer + composer (canvas id="gl")
//   const env = await G.hdr('/ABS/hdri/studio_small_09_2k.hdr');   // Poly Haven HDRI → PBR reflections
//   const S = G.scene({env, bg:'#050817'});  const cam = G.camera(30);
//   const cable = K.explodedLayers([...]);  S.add(cable.group);    // layers that come apart
//   function seek(t){ cable.set(K.ease(K.seg(t,2,4.2))); K.orbit(cam,{...}); G.render(S,cam); window.FOCAL_BOXES=()=>[G.box(cable.group,cam,'cabo')]; }
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RGBELoader} from 'three/addons/loaders/RGBELoader.js';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
export {THREE};

// ------------------------------------------------------------------ math (same names as the template)
export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), seg=(t,a,b)=>clamp((t-a)/(b-a)), lerp=(a,b,t)=>a+(b-a)*t;
export const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;          // in-out cubic — calm camera moves
export const out5=t=>1-Math.pow(1-t,5);
export const hash=n=>{const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);};   // deterministic "random"
const xhr=u=>new Promise((ok,no)=>{const x=new XMLHttpRequest();x.open('GET',u.startsWith('/')?'file://'+u:u);x.responseType='arraybuffer';
  x.onload=()=>ok(x.response);x.onerror=()=>no(new Error('load failed '+u));x.send();});
const img=u=>new Promise((ok,no)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=()=>no(new Error('img '+u));i.src=u.startsWith('/')?'file://'+u:u;});

// ------------------------------------------------------------------ renderer, loaders, composer
export async function init3D(stage,W,H,{bloom=false,bloomStrength=.55,bloomRadius=.6,bloomThreshold=.85,exposure=1}={}){
  const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true,alpha:true});
  r.setPixelRatio(1);r.setSize(W,H);r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=exposure;
  r.outputColorSpace=THREE.SRGBColorSpace;r.domElement.id='gl';
  Object.assign(r.domElement.style,{position:'absolute',left:0,top:0});stage.appendChild(r.domElement);
  const pm=new THREE.PMREMGenerator(r);
  let comp=null,bl=null;
  const G={renderer:r,W,H,
    async hdr(path){const d=new RGBELoader().parse(await xhr(path));
      const t=new THREE.DataTexture(d.data,d.width,d.height,THREE.RGBAFormat,d.type);
      t.mapping=THREE.EquirectangularReflectionMapping;t.colorSpace=THREE.LinearSRGBColorSpace;t.flipY=true;t.needsUpdate=true;
      const e=pm.fromEquirectangular(t).texture;t.dispose();return e;},
    async glb(path){return (await new GLTFLoader().parseAsync(await xhr(path),'')).scene;},
    async tex(path,{srgb=true,repeat=null}={}){const t=new THREE.Texture(await img(path));t.colorSpace=srgb?THREE.SRGBColorSpace:THREE.NoColorSpace;
      t.anisotropy=8;if(repeat){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(...repeat);}t.needsUpdate=true;return t;},
    scene({env=null,envIntensity=1,bg=null,fog=null}={}){const s=new THREE.Scene();if(env){s.environment=env;s.environmentIntensity=envIntensity;}
      if(bg)s.background=new THREE.Color(bg);if(fog)s.fog=new THREE.FogExp2(fog.color,fog.density);return s;},
    camera(fov=30,near=.05,far=200){return new THREE.PerspectiveCamera(fov,W/H,near,far);},
    render(scene,cam,{bloom:on=bloom}={}){
      if(on){if(!comp){comp=new EffectComposer(r);comp.setPixelRatio(1);comp.setSize(W,H);comp.addPass(new RenderPass(scene,cam));
          bl=new UnrealBloomPass(new THREE.Vector2(W,H),bloomStrength,bloomRadius,bloomThreshold);comp.addPass(bl);comp.addPass(new OutputPass());}
        comp.passes[0].scene=scene;comp.passes[0].camera=cam;comp.render();}
      else r.render(scene,cam);},
    setBloom(strength){if(bl)bl.strength=strength;},
    hide(){r.domElement.style.visibility='hidden';}, show(){r.domElement.style.visibility='visible';},
    // screen-space box of an object (for window.FOCAL_BOXES → render.py layout check: no text on top, not cut)
    box(obj,cam,name='3d'){obj.updateWorldMatrix(true,true);const pts=[],v=new THREE.Vector3();   // projected silhouette bounds (vertex sample)
      obj.traverse(o=>{if(!o.isMesh||!o.visible||!o.geometry.attributes.position)return;const a=o.geometry.attributes.position,st=Math.max(1,Math.floor(a.count/400));
        for(let i=0;i<a.count;i+=st){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld).project(cam);if(v.z<1)pts.push([(v.x+1)/2*W,(1-v.y)/2*H]);}});
      if(!pts.length)return {x:0,y:0,w:0,h:0,name};const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);
      const x0=Math.min(...xs),y0=Math.min(...ys);return {x:x0,y:y0,w:Math.max(...xs)-x0,h:Math.max(...ys)-y0,name};},
  };
  return G;}

// ------------------------------------------------------------------ camera moves (calm by default: span the shot, eased)
export function orbit(cam,{target=[0,0,0],radius=6,az=0,el=.25,az1=null,el1=null,r1=null,p=0}={}){
  const a=lerp(az,az1??az,ease(p)),e=lerp(el,el1??el,ease(p)),rr=lerp(radius,r1??radius,ease(p));
  cam.position.set(target[0]+rr*Math.cos(e)*Math.sin(a),target[1]+rr*Math.sin(e),target[2]+rr*Math.cos(e)*Math.cos(a));
  cam.lookAt(...target);}
export function dolly(cam,from,to,look0,look1,p){const k=ease(p);cam.position.set(...from.map((v,i)=>lerp(v,to[i],k)));
  cam.lookAt(...look0.map((v,i)=>lerp(v,look1[i],k)));}
// fit a sphere of radius R into a fraction of the frame width (portrait-safe), returns the camera distance
export function fitDistance(cam,R,frac=.85){const vf=cam.fov*Math.PI/180,hf=2*Math.atan(Math.tan(vf/2)*cam.aspect);
  return Math.max(R/Math.sin(vf/2*frac),R/Math.sin(hf/2*frac));}

// ------------------------------------------------------------------ materials
export const mat={
  metal:(c='#c8ccd6',rough=.25)=>new THREE.MeshStandardMaterial({color:c,metalness:1,roughness:rough}),
  plastic:(c='#1b1e24',rough=.45)=>new THREE.MeshStandardMaterial({color:c,metalness:0,roughness:rough}),
  copper:()=>new THREE.MeshStandardMaterial({color:'#c4743f',metalness:1,roughness:.3}),
  gold:()=>new THREE.MeshStandardMaterial({color:'#d4a94a',metalness:1,roughness:.22}),
  glass:(c='#cfe7ff')=>new THREE.MeshPhysicalMaterial({color:c,metalness:0,roughness:.05,transmission:1,thickness:.3,ior:1.45,transparent:true}),
  chrome:()=>new THREE.MeshPhysicalMaterial({color:'#dfe3ea',metalness:1,roughness:.04,clearcoat:1,clearcoatRoughness:.02}),
  emissive:(c,k=3)=>new THREE.MeshBasicMaterial({color:new THREE.Color(c).multiplyScalar(k),toneMapped:false}),  // glows under bloom
  photo:(tex)=>new THREE.MeshStandardMaterial({map:tex,roughness:.55,metalness:.1}),   // e.g. a real die shot on a chip
};

// ------------------------------------------------------------------ glow sprites, bokeh, backdrop (no flat void)
let _glow=null;
function glowTex(){if(_glow)return _glow;const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d');
  const rg=g.createRadialGradient(128,128,0,128,128,128);rg.addColorStop(0,'rgba(255,255,255,1)');rg.addColorStop(.18,'rgba(255,255,255,.55)');
  rg.addColorStop(.5,'rgba(255,255,255,.12)');rg.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=rg;g.fillRect(0,0,256,256);
  return _glow=new THREE.CanvasTexture(c);}
export function glow(color='#9cc8ff',size=1,opacity=1){const s=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex(),color,transparent:true,opacity,
  blending:THREE.AdditiveBlending,depthWrite:false,toneMapped:false}));s.scale.setScalar(size);return s;}
export function bokeh(n=40,spread=10,seed=1,color='#9cc8ff'){const g=new THREE.Group();
  for(let i=0;i<n;i++){const s=glow(color,.08+hash(seed+i*5.1)*.35,.12+.25*hash(seed+i*3.1));
    s.position.set((hash(seed+i)-.5)*spread,(hash(seed+i*1.7)-.5)*spread*1.6,-2-hash(seed+i*2.3)*8);s.userData.p=s.position.clone();g.add(s);}
  g.userData.drift=t=>g.children.forEach((s,i)=>{s.position.y=s.userData.p.y+Math.sin(t*.3+i)*.08;});return g;}
export function backdrop(c1='#0d1a3a',c2='#03050f',{z=-14,size=60}={}){const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');
  const rg=g.createRadialGradient(256,230,10,256,256,300);rg.addColorStop(0,c1);rg.addColorStop(1,c2);g.fillStyle=rg;g.fillRect(0,0,512,512);
  const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;
  const m=new THREE.Mesh(new THREE.PlaneGeometry(size,size*1.8),new THREE.MeshBasicMaterial({map:t,depthWrite:false}));m.position.z=z;return m;}
// soft volumetric light shaft (additive cone)
export function lightShaft(color='#9cc8ff',{len=12,r0=.2,r1=2.4,opacity=.08}={}){
  const m=new THREE.Mesh(new THREE.CylinderGeometry(r0,r1,len,48,1,true),new THREE.MeshBasicMaterial({color,transparent:true,opacity,
    blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,toneMapped:false}));m.geometry.translate(0,-len/2,0);return m;}

// ------------------------------------------------------------------ EXPLODED LAYERS — an object that comes apart
// layers = [{name, r0, r1, len, material}, ...] from OUTSIDE to INSIDE (concentric tubes, e.g. a cable) — or pass
// kind:'stack' with {name, w, h, d, material} boxes for a chip package (lid / die / substrate / balls).
// set(p): p=0 assembled, p=1 fully exploded (each layer slides out along the axis, staggered). Hold after exploding!
export function explodedLayers(layers,{kind='tube',gap=1.1,stagger=.12}={}){
  const group=new THREE.Group(),parts=[];
  layers.forEach((L,i)=>{let mesh;
    if(kind==='tube'){const g=new THREE.CylinderGeometry(L.r1,L.r1,L.len,96,1,!!L.r0);g.rotateZ(Math.PI/2);
      mesh=new THREE.Mesh(g,L.material);if(L.r0){const inner=new THREE.Mesh(new THREE.CylinderGeometry(L.r0,L.r0,L.len,96,1,true).rotateZ(Math.PI/2),L.material);
        inner.material=L.material.clone();inner.material.side=THREE.BackSide;mesh.add(inner);
        const cap=new THREE.Mesh(new THREE.RingGeometry(L.r0,L.r1,96).rotateY(Math.PI/2),L.material);cap.position.x=L.len/2;mesh.add(cap);}}
    else{mesh=new THREE.Mesh(new THREE.BoxGeometry(L.w,L.h,L.d),L.material);}
    mesh.name=L.name;group.add(mesh);parts.push(mesh);});
  return {group,parts,set(p){parts.forEach((m,i)=>{const k=ease(clamp((p-i*stagger)/(1-stagger*(parts.length-1)||1)));
    if(kind==='tube')m.position.x=-k*gap*(parts.length-1-i);   // outer layers slide back the most → each inner layer sticks out further (core in front)
    else m.position.y=k*gap*(parts.length-1-i);});}};}   // stack: top layers lift up

// ------------------------------------------------------------------ GLOBE — Natural Earth land texture + glowing arcs
// tex: equirectangular land texture (scripts/make_globe_texture.py). arcs: [[lat,lon,lat,lon], ...]
export function globe({tex,radius=1,ocean='#0b1f4a',atmosphere='#5cadf5'}={}){
  const g=new THREE.Group();
  const earth=new THREE.Mesh(new THREE.SphereGeometry(radius,128,96),new THREE.MeshStandardMaterial({map:tex||null,color:tex?'#ffffff':ocean,roughness:.85,metalness:.05}));
  g.add(earth);
  const atm=new THREE.Mesh(new THREE.SphereGeometry(radius*1.07,96,64),new THREE.ShaderMaterial({uniforms:{c:{value:new THREE.Color(atmosphere)}},
    vertexShader:'varying vec3 vN;void main(){vN=normalize(normalMatrix*normal);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:'uniform vec3 c;varying vec3 vN;void main(){float f=pow(.75-dot(vN,vec3(0,0,1.)),3.);gl_FragColor=vec4(c*f*1.6,f);}',
    side:THREE.BackSide,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));g.add(atm);
  const ll=(lat,lon,r=radius)=>{const p=(90-lat)*Math.PI/180,t=(lon+180)*Math.PI/180;return new THREE.Vector3(-r*Math.sin(p)*Math.cos(t),r*Math.cos(p),r*Math.sin(p)*Math.sin(t));};
  const arcs=[];
  g.userData.arc=(la1,lo1,la2,lo2,{color='#9fd2ff',lift=.25}={})=>{const a=ll(la1,lo1),b=ll(la2,lo2),m=a.clone().add(b).multiplyScalar(.5);
    m.setLength(radius*(1+lift*a.distanceTo(b)/radius));const curve=new THREE.QuadraticBezierCurve3(a,m,b);
    const geo=new THREE.TubeGeometry(curve,128,radius*.006,8);const mesh=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color:new THREE.Color(color).multiplyScalar(2),toneMapped:false}));
    mesh.geometry.setDrawRange(0,0);g.add(mesh);const o={mesh,curve,draw:p=>mesh.geometry.setDrawRange(0,Math.floor(geo.index.count*clamp(p)/6)*6)};arcs.push(o);return o;};
  g.userData.latlon=ll;g.userData.arcs=arcs;
  // rotate so (lat,lon) faces the camera (+z): g.rotation.y = K.globeFace(lon)
  return g;}
export const globeFace=lon=>-(lon+90)*Math.PI/180;

// ------------------------------------------------------------------ SEABED / FLOOR — a long object lying on a textured floor
// floorTex: e.g. Poly Haven "aerial_beach" / sand diffuse; fog gives depth; read it 3/4 from the side so it reads at a glance
export function floor({tex=null,color='#1d2a33',size=80,repeat=12}={}){
  if(tex){tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.repeat.set(repeat,repeat);}
  const m=new THREE.Mesh(new THREE.PlaneGeometry(size,size,1,1),new THREE.MeshStandardMaterial({map:tex,color:tex?'#ffffff':color,roughness:.95}));
  m.rotation.x=-Math.PI/2;return m;}
// a long cable/pipe following points, with a helical armour texture feel (bump via a stripe canvas)
export function longCable(points,{radius=.09,color='#2b2f36'}={}){
  const c=document.createElement('canvas');c.width=512;c.height=64;const g=c.getContext('2d');g.fillStyle=color;g.fillRect(0,0,512,64);
  for(let x=-64;x<512;x+=10){g.strokeStyle='rgba(255,255,255,.10)';g.lineWidth=3;g.beginPath();g.moveTo(x,0);g.lineTo(x+64,64);g.stroke();}
  const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(60,1);t.colorSpace=THREE.SRGBColorSpace;
  const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));
  const mesh=new THREE.Mesh(new THREE.TubeGeometry(curve,400,radius,24),new THREE.MeshStandardMaterial({map:t,roughness:.55,metalness:.35}));
  // a pulse of light that travels along it: pulse.set(p) with p in 0..1
  const pulse=glow('#bfe3ff',radius*12,1);mesh.add(pulse);
  return {mesh,curve,pulse,setPulse(p,on=1){pulse.position.copy(curve.getPointAt(clamp(p)));pulse.material.opacity=on;}};}

// ------------------------------------------------------------------ photo plane (a real photo as a card in 3D, with parallax)
export function photoPlane(tex,height=2){const a=tex.image.width/tex.image.height;
  return new THREE.Mesh(new THREE.PlaneGeometry(height*a,height),new THREE.MeshBasicMaterial({map:tex,toneMapped:false}));}
