!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?exports.miniplayer=e():(t.xgplayer=t.xgplayer||{},t.xgplayer.PlayerControls=t.xgplayer.PlayerControls||{},t.xgplayer.PlayerControls.miniplayer=e())}(window,(function(){return function(t){var e={};function n(i){if(e[i])return e[i].exports;var o=e[i]={i:i,l:!1,exports:{}};return t[i].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=t,n.c=e,n.d=function(t,e,i){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)n.d(i,o,function(e){return t[e]}.bind(null,o));return i},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=1)}([function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.util=e.PresentationMode=void 0,e.createDom=s,e.hasClass=a,e.addClass=l,e.removeClass=c,e.toggleClass=u,e.findDom=h,e.padStart=d,e.format=f,e.event=p,e.typeOf=g,e.deepCopy=v,e.getBgImage=y,e.copyDom=m,e._setInterval=b,e._clearInterval=x,e.createImgBtn=w,e.isWeiXin=E,e.isUc=_,e.computeWatchDur=P,e.offInDestroy=C,e.on=M,e.once=D,e.getBuffered2=S,e.checkIsBrowser=L,e.setStyle=k,e.checkWebkitSetPresentationMode=function(t){return"function"==typeof t.webkitSetPresentationMode};var i,o=n(3),r=(i=o)&&i.__esModule?i:{default:i};function s(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"div",e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"",n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},i=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"",o=document.createElement(t);return o.className=i,o.innerHTML=e,Object.keys(n).forEach((function(e){var i=e,r=n[e];"video"===t||"audio"===t?r&&o.setAttribute(i,r):o.setAttribute(i,r)})),o}function a(t,e){return!!t&&(t.classList?Array.prototype.some.call(t.classList,(function(t){return t===e})):!!t.className&&!!t.className.match(new RegExp("(\\s|^)"+e+"(\\s|$)")))}function l(t,e){t&&(t.classList?e.replace(/(^\s+|\s+$)/g,"").split(/\s+/g).forEach((function(e){e&&t.classList.add(e)})):a(t,e)||(t.className+=" "+e))}function c(t,e){t&&(t.classList?e.split(/\s+/g).forEach((function(e){t.classList.remove(e)})):a(t,e)&&e.split(/\s+/g).forEach((function(e){var n=new RegExp("(\\s|^)"+e+"(\\s|$)");t.className=t.className.replace(n," ")})))}function u(t,e){t&&e.split(/\s+/g).forEach((function(e){a(t,e)?c(t,e):l(t,e)}))}function h(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:document,e=arguments[1],n=void 0;try{n=t.querySelector(e)}catch(i){0===e.indexOf("#")&&(n=t.getElementById(e.slice(1)))}return n}function d(t,e,n){for(var i=String(n),o=e>>0,r=Math.ceil(o/i.length),s=[],a=String(t);r--;)s.push(i);return s.join("").substring(0,o-a.length)+a}function f(t){if(window.isNaN(t))return"";var e=d(Math.floor(t/3600),2,0),n=d(Math.floor((t-3600*e)/60),2,0),i=d(Math.floor(t-3600*e-60*n),2,0);return("00"===e?[n,i]:[e,n,i]).join(":")}function p(t){if(t.touches){var e=t.touches[0]||t.changedTouches[0];t.clientX=e.clientX||0,t.clientY=e.clientY||0,t.offsetX=e.pageX-e.target.offsetLeft,t.offsetY=e.pageY-e.target.offsetTop}t._target=t.target||t.srcElement}function g(t){return Object.prototype.toString.call(t).match(/([^\s.*]+)(?=]$)/g)[0]}function v(t,e){if("Object"===g(e)&&"Object"===g(t))return Object.keys(e).forEach((function(n){"Object"!==g(e[n])||e[n]instanceof Node?"Array"===g(e[n])?t[n]="Array"===g(t[n])?t[n].concat(e[n]):e[n]:t[n]=e[n]:t[n]?v(t[n],e[n]):t[n]=e[n]})),t}function y(t){var e=(t.currentStyle||window.getComputedStyle(t,null)).backgroundImage;if(!e||"none"===e)return"";var n=document.createElement("a");return n.href=e.replace(/url\("|"\)/g,""),n.href}function m(t){if(t&&1===t.nodeType){var e=document.createElement(t.tagName);return Array.prototype.forEach.call(t.attributes,(function(t){e.setAttribute(t.name,t.value)})),t.innerHTML&&(e.innerHTML=t.innerHTML),e}return""}function b(t,e,n,i){t._interval[e]||(t._interval[e]=setInterval(n.bind(t),i))}function x(t,e){clearInterval(t._interval[e]),t._interval[e]=null}function w(t,e,n,i){var o=s("xg-"+t,"",{},"xgplayer-"+t+"-img");if(o.style.backgroundImage='url("'+e+'")',n&&i){var r=void 0,a=void 0,l=void 0;["px","rem","em","pt","dp","vw","vh","vm","%"].every((function(t){return!(n.indexOf(t)>-1&&i.indexOf(t)>-1)||(r=Number(n.slice(0,n.indexOf(t)).trim()),a=Number(i.slice(0,i.indexOf(t)).trim()),l=t,!1)})),o.style.width=""+r+l,o.style.height=""+a+l,o.style.backgroundSize=""+r+l+" "+a+l,o.style.margin="start"===t?"-"+a/2+l+" auto auto -"+r/2+l:"auto 5px auto 5px"}return o}function E(){return window.navigator.userAgent.toLowerCase().indexOf("micromessenger")>-1}function _(){return window.navigator.userAgent.toLowerCase().indexOf("ucbrowser")>-1}function P(){for(var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],e=[],n=0;n<t.length;n++)if(!(!t[n].end||t[n].begin<0||t[n].end<0||t[n].end<t[n].begin))if(e.length<1)e.push({begin:t[n].begin,end:t[n].end});else for(var i=0;i<e.length;i++){var o=t[n].begin,r=t[n].end;if(r<e[i].begin){e.splice(i,0,{begin:o,end:r});break}if(!(o>e[i].end)){var s=e[i].begin,a=e[i].end;e[i].begin=Math.min(o,s),e[i].end=Math.max(r,a);break}if(i>e.length-2){e.push({begin:o,end:r});break}}for(var l=0,c=0;c<e.length;c++)l+=e[c].end-e[c].begin;return l}function C(t,e,n,i){t.once(i,(function o(){t.off(e,n),t.off(i,o)}))}function M(t,e,n,i){if(i)t.on(e,n),C(t,e,n,i);else{t.on(e,(function i(o){n(o),t.off(e,i)}))}}function D(t,e,n,i){if(i)t.once(e,n),C(t,e,n,i);else{t.once(e,(function i(o){n(o),t.off(e,i)}))}}function S(t){for(var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:.5,n=[],i=0;i<t.length;i++)n.push({start:t.start(i)<.5?0:t.start(i),end:t.end(i)});n.sort((function(t,e){var n=t.start-e.start;return n||e.end-t.end}));var o=[];if(e)for(var s=0;s<n.length;s++){var a=o.length;if(a){var l=o[a-1].end;n[s].start-l<e?n[s].end>l&&(o[a-1].end=n[s].end):o.push(n[s])}else o.push(n[s])}else o=n;return new r.default(o)}function L(){return!("undefined"==typeof window||void 0===window.document||void 0===window.document.createElement)}function k(t,e,n){var i=t.style;try{i[e]=n}catch(t){i.setProperty(e,n)}}e.PresentationMode={PIP:"picture-in-picture",INLINE:"inline",FULLSCREEN:"fullscreen"};e.util={createDom:s,hasClass:a,addClass:l,removeClass:c,toggleClass:u,findDom:h,padStart:d,format:f,event:p,typeOf:g,deepCopy:v,getBgImage:y,copyDom:m,setInterval:b,clearInterval:x,createImgBtn:w,isWeiXin:E,isUc:_,computeWatchDur:P,offInDestroy:C,on:M,once:D,getBuffered2:S,checkIsBrowser:L,setStyle:k}},function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=r(n(2)),o=r(n(9));function r(t){return t&&t.__esModule?t:{default:t}}e.default={name:"miniplayer",method:function(){i.default.method.call(this),o.default.method.call(this)}},t.exports=e.default},function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i,o=n(0),r=n(4),s=(i=r)&&i.__esModule?i:{default:i};e.default={name:"miniplayer",method:function(){var t=this,e=t.root;function n(){(0,o.hasClass)(e,"xgplayer-miniplayer-active")?t.exitMiniplayer():t.getMiniplayer()}t.on("miniplayerBtnClick",n),t.once("destroy",(function e(){t.off("miniplayerBtnClick",n),t.off("destroy",e)})),t.getMiniplayer=function(){(0,o.hasClass)(e,"xgplayer-is-fullscreen")&&this.exitFullscreen(e),(0,o.hasClass)(e,"xgplayer-is-cssfullscreen")&&this.exitCssFullscreen(),(0,o.hasClass)(e,"xgplayer-rotate-fullscreen")&&this.exitRotateFullscreen();var t=(0,o.createDom)("xg-miniplayer-lay","<div></div>",{},"xgplayer-miniplayer-lay");this.root.appendChild(t);var n=(0,o.createDom)("xg-miniplayer-drag",'<div class="drag-handle"><span>'+this.lang.MINIPLAYER_DRAG+"</span></div>",{tabindex:9},"xgplayer-miniplayer-drag");this.root.appendChild(n);new s.default(".xgplayer",{handle:".drag-handle"});(0,o.addClass)(this.root,"xgplayer-miniplayer-active"),this.root.style.right=0,this.root.style.bottom="200px",this.root.style.top="",this.root.style.left="",this.root.style.width="320px",this.root.style.height="180px",this.config.miniplayerConfig&&(void 0!==this.config.miniplayerConfig.top&&(this.root.style.top=this.config.miniplayerConfig.top+"px",this.root.style.bottom=""),void 0!==this.config.miniplayerConfig.bottom&&(this.root.style.bottom=this.config.miniplayerConfig.bottom+"px"),void 0!==this.config.miniplayerConfig.left&&(this.root.style.left=this.config.miniplayerConfig.left+"px",this.root.style.right=""),void 0!==this.config.miniplayerConfig.right&&(this.root.style.right=this.config.miniplayerConfig.right+"px"),void 0!==this.config.miniplayerConfig.width&&(this.root.style.width=this.config.miniplayerConfig.width+"px"),void 0!==this.config.miniplayerConfig.height&&(this.root.style.height=this.config.miniplayerConfig.height+"px")),this.config.fluid&&(this.root.style["padding-top"]="");var i=this;["click","touchend"].forEach((function(e){t.addEventListener(e,(function(t){t.preventDefault(),t.stopPropagation(),i.exitMiniplayer()}))}))},t.exitMiniplayer=function(){(0,o.removeClass)(this.root,"xgplayer-miniplayer-active"),this.root.style.right="",this.root.style.bottom="",this.root.style.top="",this.root.style.left="",this.config.fluid?(this.root.style.width="100%",this.root.style.height="0",this.root.style["padding-top"]=100*this.config.height/this.config.width+"%"):(this.config.width&&("number"!=typeof this.config.width?this.root.style.width=this.config.width:this.root.style.width=this.config.width+"px"),this.config.height&&("number"!=typeof this.config.height?this.root.style.height=this.config.height:this.root.style.height=this.config.height+"px"));var t=(0,o.findDom)(this.root,".xgplayer-miniplayer-lay");t&&t.parentNode&&t.parentNode.removeChild(t);var e=(0,o.findDom)(this.root,".xgplayer-miniplayer-drag");e&&e.parentNode&&e.parentNode.removeChild(e)}}},t.exports=e.default},function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}();var o=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.bufferedList=e}return i(t,[{key:"start",value:function(t){return this.bufferedList[t].start}},{key:"end",value:function(t){return this.bufferedList[t].end}},{key:"length",get:function(){return this.bufferedList.length}}]),t}();e.default=o,t.exports=e.default},function(t,e,n){var i,o;
/*!
 * Draggabilly v2.3.0
 * Make that shiz draggable
 * https://draggabilly.desandro.com
 * MIT license
 */!function(r,s){i=[n(5),n(6)],void 0===(o=function(t,e){return function(t,e,n){function i(t,e){for(var n in e)t[n]=e[n];return t}var o=t.jQuery;function r(t,e){this.element="string"==typeof t?document.querySelector(t):t,o&&(this.$element=o(this.element)),this.options=i({},this.constructor.defaults),this.option(e),this._create()}var s=r.prototype=Object.create(n.prototype);r.defaults={},s.option=function(t){i(this.options,t)};var a={relative:!0,absolute:!0,fixed:!0};function l(t,e,n){return n=n||"round",e?Math[n](t/e)*e:t}s._create=function(){this.position={},this._getPosition(),this.startPoint={x:0,y:0},this.dragPoint={x:0,y:0},this.startPosition=i({},this.position);var t=getComputedStyle(this.element);a[t.position]||(this.element.style.position="relative"),this.on("pointerMove",this.onPointerMove),this.on("pointerUp",this.onPointerUp),this.enable(),this.setHandles()},s.setHandles=function(){this.handles=this.options.handle?this.element.querySelectorAll(this.options.handle):[this.element],this.bindHandles()},s.dispatchEvent=function(t,e,n){var i=[e].concat(n);this.emitEvent(t,i),this.dispatchJQueryEvent(t,e,n)},s.dispatchJQueryEvent=function(e,n,i){var o=t.jQuery;if(o&&this.$element){var r=o.Event(n);r.type=e,this.$element.trigger(r,i)}},s._getPosition=function(){var t=getComputedStyle(this.element),e=this._getPositionCoord(t.left,"width"),n=this._getPositionCoord(t.top,"height");this.position.x=isNaN(e)?0:e,this.position.y=isNaN(n)?0:n,this._addTransformPosition(t)},s._getPositionCoord=function(t,n){if(-1!=t.indexOf("%")){var i=e(this.element.parentNode);return i?parseFloat(t)/100*i[n]:0}return parseInt(t,10)},s._addTransformPosition=function(t){var e=t.transform;if(0===e.indexOf("matrix")){var n=e.split(","),i=0===e.indexOf("matrix3d")?12:4,o=parseInt(n[i],10),r=parseInt(n[i+1],10);this.position.x+=o,this.position.y+=r}},s.onPointerDown=function(t,e){this.element.classList.add("is-pointer-down"),this.dispatchJQueryEvent("pointerDown",t,[e])},s.pointerDown=function(t,e){this.okayPointerDown(t)&&this.isEnabled?(this.pointerDownPointer={pageX:e.pageX,pageY:e.pageY},t.preventDefault(),this.pointerDownBlur(),this._bindPostStartEvents(t),this.element.classList.add("is-pointer-down"),this.dispatchEvent("pointerDown",t,[e])):this._pointerReset()},s.dragStart=function(t,e){this.isEnabled&&(this._getPosition(),this.measureContainment(),this.startPosition.x=this.position.x,this.startPosition.y=this.position.y,this.setLeftTop(),this.dragPoint.x=0,this.dragPoint.y=0,this.element.classList.add("is-dragging"),this.dispatchEvent("dragStart",t,[e]),this.animate())},s.measureContainment=function(){var t=this.getContainer();if(t){var n=e(this.element),i=e(t),o=this.element.getBoundingClientRect(),r=t.getBoundingClientRect(),s=i.borderLeftWidth+i.borderRightWidth,a=i.borderTopWidth+i.borderBottomWidth,l=this.relativeStartPosition={x:o.left-(r.left+i.borderLeftWidth),y:o.top-(r.top+i.borderTopWidth)};this.containSize={width:i.width-s-l.x-n.width,height:i.height-a-l.y-n.height}}},s.getContainer=function(){var t=this.options.containment;if(t)return t instanceof HTMLElement?t:"string"==typeof t?document.querySelector(t):this.element.parentNode},s.onPointerMove=function(t,e,n){this.dispatchJQueryEvent("pointerMove",t,[e,n])},s.dragMove=function(t,e,n){if(this.isEnabled){var i=n.x,o=n.y,r=this.options.grid,s=r&&r[0],a=r&&r[1];i=l(i,s),o=l(o,a),i=this.containDrag("x",i,s),o=this.containDrag("y",o,a),i="y"==this.options.axis?0:i,o="x"==this.options.axis?0:o,this.position.x=this.startPosition.x+i,this.position.y=this.startPosition.y+o,this.dragPoint.x=i,this.dragPoint.y=o,this.dispatchEvent("dragMove",t,[e,n])}},s.containDrag=function(t,e,n){if(!this.options.containment)return e;var i="x"==t?"width":"height",o=l(-this.relativeStartPosition[t],n,"ceil"),r=this.containSize[i];return r=l(r,n,"floor"),Math.max(o,Math.min(r,e))},s.onPointerUp=function(t,e){this.element.classList.remove("is-pointer-down"),this.dispatchJQueryEvent("pointerUp",t,[e])},s.dragEnd=function(t,e){this.isEnabled&&(this.element.style.transform="",this.setLeftTop(),this.element.classList.remove("is-dragging"),this.dispatchEvent("dragEnd",t,[e]))},s.animate=function(){if(this.isDragging){this.positionDrag();var t=this;requestAnimationFrame((function(){t.animate()}))}},s.setLeftTop=function(){this.element.style.left=this.position.x+"px",this.element.style.top=this.position.y+"px"},s.positionDrag=function(){this.element.style.transform="translate3d( "+this.dragPoint.x+"px, "+this.dragPoint.y+"px, 0)"},s.staticClick=function(t,e){this.dispatchEvent("staticClick",t,[e])},s.setPosition=function(t,e){this.position.x=t,this.position.y=e,this.setLeftTop()},s.enable=function(){this.isEnabled=!0},s.disable=function(){this.isEnabled=!1,this.isDragging&&this.dragEnd()},s.destroy=function(){this.disable(),this.element.style.transform="",this.element.style.left="",this.element.style.top="",this.element.style.position="",this.unbindHandles(),this.$element&&this.$element.removeData("draggabilly")},s._init=function(){},o&&o.bridget&&o.bridget("draggabilly",r);return r}(r,t,e)}.apply(e,i))||(t.exports=o)}(window)},function(t,e,n){var i,o;
/*!
 * getSize v2.0.3
 * measure size of elements
 * MIT license
 */window,void 0===(o="function"==typeof(i=function(){"use strict";function t(t){var e=parseFloat(t);return-1==t.indexOf("%")&&!isNaN(e)&&e}var e="undefined"==typeof console?function(){}:function(t){console.error(t)},n=["paddingLeft","paddingRight","paddingTop","paddingBottom","marginLeft","marginRight","marginTop","marginBottom","borderLeftWidth","borderRightWidth","borderTopWidth","borderBottomWidth"],i=n.length;function o(t){var n=getComputedStyle(t);return n||e("Style returned "+n+". Are you running this code in a hidden iframe on Firefox? See https://bit.ly/getsizebug1"),n}var r,s=!1;function a(e){if(function(){if(!s){s=!0;var e=document.createElement("div");e.style.width="200px",e.style.padding="1px 2px 3px 4px",e.style.borderStyle="solid",e.style.borderWidth="1px 2px 3px 4px",e.style.boxSizing="border-box";var n=document.body||document.documentElement;n.appendChild(e);var i=o(e);r=200==Math.round(t(i.width)),a.isBoxSizeOuter=r,n.removeChild(e)}}(),"string"==typeof e&&(e=document.querySelector(e)),e&&"object"==typeof e&&e.nodeType){var l=o(e);if("none"==l.display)return function(){for(var t={width:0,height:0,innerWidth:0,innerHeight:0,outerWidth:0,outerHeight:0},e=0;e<i;e++)t[n[e]]=0;return t}();var c={};c.width=e.offsetWidth,c.height=e.offsetHeight;for(var u=c.isBorderBox="border-box"==l.boxSizing,h=0;h<i;h++){var d=n[h],f=l[d],p=parseFloat(f);c[d]=isNaN(p)?0:p}var g=c.paddingLeft+c.paddingRight,v=c.paddingTop+c.paddingBottom,y=c.marginLeft+c.marginRight,m=c.marginTop+c.marginBottom,b=c.borderLeftWidth+c.borderRightWidth,x=c.borderTopWidth+c.borderBottomWidth,w=u&&r,E=t(l.width);!1!==E&&(c.width=E+(w?0:g+b));var _=t(l.height);return!1!==_&&(c.height=_+(w?0:v+x)),c.innerWidth=c.width-(g+b),c.innerHeight=c.height-(v+x),c.outerWidth=c.width+y,c.outerHeight=c.height+m,c}}return a})?i.call(e,n,e,t):i)||(t.exports=o)},function(t,e,n){var i,o;
/*!
 * Unidragger v2.3.1
 * Draggable base class
 * MIT license
 */!function(r,s){i=[n(7)],void 0===(o=function(t){return function(t,e){"use strict";function n(){}var i=n.prototype=Object.create(e.prototype);i.bindHandles=function(){this._bindHandles(!0)},i.unbindHandles=function(){this._bindHandles(!1)},i._bindHandles=function(e){for(var n=(e=void 0===e||e)?"addEventListener":"removeEventListener",i=e?this._touchActionValue:"",o=0;o<this.handles.length;o++){var r=this.handles[o];this._bindStartEvent(r,e),r[n]("click",this),t.PointerEvent&&(r.style.touchAction=i)}},i._touchActionValue="none",i.pointerDown=function(t,e){this.okayPointerDown(t)&&(this.pointerDownPointer={pageX:e.pageX,pageY:e.pageY},t.preventDefault(),this.pointerDownBlur(),this._bindPostStartEvents(t),this.emitEvent("pointerDown",[t,e]))};var o={TEXTAREA:!0,INPUT:!0,SELECT:!0,OPTION:!0},r={radio:!0,checkbox:!0,button:!0,submit:!0,image:!0,file:!0};return i.okayPointerDown=function(t){var e=o[t.target.nodeName],n=r[t.target.type],i=!e||n;return i||this._pointerReset(),i},i.pointerDownBlur=function(){var t=document.activeElement;t&&t.blur&&t!=document.body&&t.blur()},i.pointerMove=function(t,e){var n=this._dragPointerMove(t,e);this.emitEvent("pointerMove",[t,e,n]),this._dragMove(t,e,n)},i._dragPointerMove=function(t,e){var n={x:e.pageX-this.pointerDownPointer.pageX,y:e.pageY-this.pointerDownPointer.pageY};return!this.isDragging&&this.hasDragStarted(n)&&this._dragStart(t,e),n},i.hasDragStarted=function(t){return Math.abs(t.x)>3||Math.abs(t.y)>3},i.pointerUp=function(t,e){this.emitEvent("pointerUp",[t,e]),this._dragPointerUp(t,e)},i._dragPointerUp=function(t,e){this.isDragging?this._dragEnd(t,e):this._staticClick(t,e)},i._dragStart=function(t,e){this.isDragging=!0,this.isPreventingClicks=!0,this.dragStart(t,e)},i.dragStart=function(t,e){this.emitEvent("dragStart",[t,e])},i._dragMove=function(t,e,n){this.isDragging&&this.dragMove(t,e,n)},i.dragMove=function(t,e,n){t.preventDefault(),this.emitEvent("dragMove",[t,e,n])},i._dragEnd=function(t,e){this.isDragging=!1,setTimeout(function(){delete this.isPreventingClicks}.bind(this)),this.dragEnd(t,e)},i.dragEnd=function(t,e){this.emitEvent("dragEnd",[t,e])},i.onclick=function(t){this.isPreventingClicks&&t.preventDefault()},i._staticClick=function(t,e){this.isIgnoringMouseUp&&"mouseup"==t.type||(this.staticClick(t,e),"mouseup"!=t.type&&(this.isIgnoringMouseUp=!0,setTimeout(function(){delete this.isIgnoringMouseUp}.bind(this),400)))},i.staticClick=function(t,e){this.emitEvent("staticClick",[t,e])},n.getPointerPoint=e.getPointerPoint,n}(r,t)}.apply(e,i))||(t.exports=o)}(window)},function(t,e,n){var i,o;
/*!
 * Unipointer v2.3.0
 * base class for doing one thing with pointer event
 * MIT license
 */!function(r,s){i=[n(8)],void 0===(o=function(t){return function(t,e){"use strict";function n(){}var i=n.prototype=Object.create(e.prototype);i.bindStartEvent=function(t){this._bindStartEvent(t,!0)},i.unbindStartEvent=function(t){this._bindStartEvent(t,!1)},i._bindStartEvent=function(e,n){var i=(n=void 0===n||n)?"addEventListener":"removeEventListener",o="mousedown";t.PointerEvent?o="pointerdown":"ontouchstart"in t&&(o="touchstart"),e[i](o,this)},i.handleEvent=function(t){var e="on"+t.type;this[e]&&this[e](t)},i.getTouch=function(t){for(var e=0;e<t.length;e++){var n=t[e];if(n.identifier==this.pointerIdentifier)return n}},i.onmousedown=function(t){var e=t.button;e&&0!==e&&1!==e||this._pointerDown(t,t)},i.ontouchstart=function(t){this._pointerDown(t,t.changedTouches[0])},i.onpointerdown=function(t){this._pointerDown(t,t)},i._pointerDown=function(t,e){t.button||this.isPointerDown||(this.isPointerDown=!0,this.pointerIdentifier=void 0!==e.pointerId?e.pointerId:e.identifier,this.pointerDown(t,e))},i.pointerDown=function(t,e){this._bindPostStartEvents(t),this.emitEvent("pointerDown",[t,e])};var o={mousedown:["mousemove","mouseup"],touchstart:["touchmove","touchend","touchcancel"],pointerdown:["pointermove","pointerup","pointercancel"]};return i._bindPostStartEvents=function(e){if(e){var n=o[e.type];n.forEach((function(e){t.addEventListener(e,this)}),this),this._boundPointerEvents=n}},i._unbindPostStartEvents=function(){this._boundPointerEvents&&(this._boundPointerEvents.forEach((function(e){t.removeEventListener(e,this)}),this),delete this._boundPointerEvents)},i.onmousemove=function(t){this._pointerMove(t,t)},i.onpointermove=function(t){t.pointerId==this.pointerIdentifier&&this._pointerMove(t,t)},i.ontouchmove=function(t){var e=this.getTouch(t.changedTouches);e&&this._pointerMove(t,e)},i._pointerMove=function(t,e){this.pointerMove(t,e)},i.pointerMove=function(t,e){this.emitEvent("pointerMove",[t,e])},i.onmouseup=function(t){this._pointerUp(t,t)},i.onpointerup=function(t){t.pointerId==this.pointerIdentifier&&this._pointerUp(t,t)},i.ontouchend=function(t){var e=this.getTouch(t.changedTouches);e&&this._pointerUp(t,e)},i._pointerUp=function(t,e){this._pointerDone(),this.pointerUp(t,e)},i.pointerUp=function(t,e){this.emitEvent("pointerUp",[t,e])},i._pointerDone=function(){this._pointerReset(),this._unbindPostStartEvents(),this.pointerDone()},i._pointerReset=function(){this.isPointerDown=!1,delete this.pointerIdentifier},i.pointerDone=function(){},i.onpointercancel=function(t){t.pointerId==this.pointerIdentifier&&this._pointerCancel(t,t)},i.ontouchcancel=function(t){var e=this.getTouch(t.changedTouches);e&&this._pointerCancel(t,e)},i._pointerCancel=function(t,e){this._pointerDone(),this.pointerCancel(t,e)},i.pointerCancel=function(t,e){this.emitEvent("pointerCancel",[t,e])},n.getPointerPoint=function(t){return{x:t.pageX,y:t.pageY}},n}(r,t)}.apply(e,i))||(t.exports=o)}(window)},function(t,e,n){var i,o;"undefined"!=typeof window&&window,void 0===(o="function"==typeof(i=function(){"use strict";function t(){}var e=t.prototype;return e.on=function(t,e){if(t&&e){var n=this._events=this._events||{},i=n[t]=n[t]||[];return-1==i.indexOf(e)&&i.push(e),this}},e.once=function(t,e){if(t&&e){this.on(t,e);var n=this._onceEvents=this._onceEvents||{};return(n[t]=n[t]||{})[e]=!0,this}},e.off=function(t,e){var n=this._events&&this._events[t];if(n&&n.length){var i=n.indexOf(e);return-1!=i&&n.splice(i,1),this}},e.emitEvent=function(t,e){var n=this._events&&this._events[t];if(n&&n.length){n=n.slice(0),e=e||[];for(var i=this._onceEvents&&this._onceEvents[t],o=0;o<n.length;o++){var r=n[o];i&&i[r]&&(this.off(t,r),delete i[r]),r.apply(this,e)}return this}},e.allOff=function(){delete this._events,delete this._onceEvents},t})?i.call(e,n,e,t):i)||(t.exports=o)},function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n(0);n(10);e.default={name:"s_miniplayer",method:function(){var t=this;if(t.config.miniplayer){var e=t.lang.MINIPLAYER,n=(0,i.createDom)("xg-miniplayer",'<p class="name"><span>'+e+"</span></p>",{tabindex:9},"xgplayer-miniplayer");t.once("ready",(function(){t.controls.appendChild(n)})),["click","touchend"].forEach((function(e){n.addEventListener(e,(function(e){e.preventDefault(),e.stopPropagation(),t.userGestureTrigEvent("miniplayerBtnClick")}))}))}}},t.exports=e.default},function(t,e,n){var i=n(11);"string"==typeof i&&(i=[[t.i,i,""]]);var o={hmr:!0,transform:void 0,insertInto:void 0};n(13)(i,o);i.locals&&(t.exports=i.locals)},function(t,e,n){(t.exports=n(12)(!1)).push([t.i,".xgplayer-skin-default .xgplayer-miniplayer{-webkit-order:9;-moz-box-ordinal-group:10;order:9;position:relative;outline:none;display:block;cursor:pointer;height:20px;top:10px}.xgplayer-skin-default .xgplayer-miniplayer .name{text-align:center;font-family:PingFangSC-Regular;font-size:13px;line-height:20px;height:20px;color:hsla(0,0%,100%,.8)}.xgplayer-skin-default .xgplayer-miniplayer .name span{width:80px;height:20px;line-height:20px;background:rgba(0,0,0,.38);border-radius:10px;display:inline-block;vertical-align:middle}.xgplayer-skin-default .xgplayer-miniplayer-lay{position:absolute;top:26px;left:0;width:100%;height:100%;z-index:130;cursor:pointer;background-color:transparent;display:none}.xgplayer-skin-default .xgplayer-miniplayer-lay div{width:100%;height:100%}.xgplayer-skin-default .xgplayer-miniplayer-drag{cursor:move;position:absolute;top:0;left:0;width:100%;height:26px;line-height:26px;background-image:linear-gradient(rgba(0,0,0,.3),transparent);z-index:130;display:none}.xgplayer-skin-default .xgplayer-miniplayer-drag .drag-handle{width:100%}.xgplayer-skin-default.xgplayer-miniplayer-active{position:fixed;right:0;bottom:200px;width:320px;height:180px;z-index:110}.xgplayer-skin-default.xgplayer-miniplayer-active .xgplayer-controls,.xgplayer-skin-default.xgplayer-miniplayer-active .xgplayer-danmu{display:none}.xgplayer-skin-default.xgplayer-miniplayer-active .xgplayer-miniplayer-lay{display:block}.xgplayer-skin-default.xgplayer-miniplayer-active .xgplayer-miniplayer-drag{display:-webkit-flex;display:-moz-box;display:flex}.xgplayer-skin-default.xgplayer-inactive .xgplayer-miniplayer-drag{display:none}.lang-is-jp .xgplayer-miniplayer .name span{width:70px;height:20px}",""])},function(t,e){t.exports=function(t){var e=[];return e.toString=function(){return this.map((function(e){var n=function(t,e){var n=t[1]||"",i=t[3];if(!i)return n;if(e&&"function"==typeof btoa){var o=(s=i,"/*# sourceMappingURL=data:application/json;charset=utf-8;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(s))))+" */"),r=i.sources.map((function(t){return"/*# sourceURL="+i.sourceRoot+t+" */"}));return[n].concat(r).concat([o]).join("\n")}var s;return[n].join("\n")}(e,t);return e[2]?"@media "+e[2]+"{"+n+"}":n})).join("")},e.i=function(t,n){"string"==typeof t&&(t=[[null,t,""]]);for(var i={},o=0;o<this.length;o++){var r=this[o][0];"number"==typeof r&&(i[r]=!0)}for(o=0;o<t.length;o++){var s=t[o];"number"==typeof s[0]&&i[s[0]]||(n&&!s[2]?s[2]=n:n&&(s[2]="("+s[2]+") and ("+n+")"),e.push(s))}},e}},function(t,e,n){var i,o,r={},s=(i=function(){return window&&document&&document.all&&!window.atob},function(){return void 0===o&&(o=i.apply(this,arguments)),o}),a=function(t){return document.querySelector(t)},l=function(t){var e={};return function(t){if("function"==typeof t)return t();if(void 0===e[t]){var n=a.call(this,t);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(t){n=null}e[t]=n}return e[t]}}(),c=null,u=0,h=[],d=n(14);function f(t,e){for(var n=0;n<t.length;n++){var i=t[n],o=r[i.id];if(o){o.refs++;for(var s=0;s<o.parts.length;s++)o.parts[s](i.parts[s]);for(;s<i.parts.length;s++)o.parts.push(b(i.parts[s],e))}else{var a=[];for(s=0;s<i.parts.length;s++)a.push(b(i.parts[s],e));r[i.id]={id:i.id,refs:1,parts:a}}}}function p(t,e){for(var n=[],i={},o=0;o<t.length;o++){var r=t[o],s=e.base?r[0]+e.base:r[0],a={css:r[1],media:r[2],sourceMap:r[3]};i[s]?i[s].parts.push(a):n.push(i[s]={id:s,parts:[a]})}return n}function g(t,e){var n=l(t.insertInto);if(!n)throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");var i=h[h.length-1];if("top"===t.insertAt)i?i.nextSibling?n.insertBefore(e,i.nextSibling):n.appendChild(e):n.insertBefore(e,n.firstChild),h.push(e);else if("bottom"===t.insertAt)n.appendChild(e);else{if("object"!=typeof t.insertAt||!t.insertAt.before)throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");var o=l(t.insertInto+" "+t.insertAt.before);n.insertBefore(e,o)}}function v(t){if(null===t.parentNode)return!1;t.parentNode.removeChild(t);var e=h.indexOf(t);e>=0&&h.splice(e,1)}function y(t){var e=document.createElement("style");return t.attrs.type="text/css",m(e,t.attrs),g(t,e),e}function m(t,e){Object.keys(e).forEach((function(n){t.setAttribute(n,e[n])}))}function b(t,e){var n,i,o,r;if(e.transform&&t.css){if(!(r=e.transform(t.css)))return function(){};t.css=r}if(e.singleton){var s=u++;n=c||(c=y(e)),i=E.bind(null,n,s,!1),o=E.bind(null,n,s,!0)}else t.sourceMap&&"function"==typeof URL&&"function"==typeof URL.createObjectURL&&"function"==typeof URL.revokeObjectURL&&"function"==typeof Blob&&"function"==typeof btoa?(n=function(t){var e=document.createElement("link");return t.attrs.type="text/css",t.attrs.rel="stylesheet",m(e,t.attrs),g(t,e),e}(e),i=P.bind(null,n,e),o=function(){v(n),n.href&&URL.revokeObjectURL(n.href)}):(n=y(e),i=_.bind(null,n),o=function(){v(n)});return i(t),function(e){if(e){if(e.css===t.css&&e.media===t.media&&e.sourceMap===t.sourceMap)return;i(t=e)}else o()}}t.exports=function(t,e){if("undefined"!=typeof DEBUG&&DEBUG&&"object"!=typeof document)throw new Error("The style-loader cannot be used in a non-browser environment");(e=e||{}).attrs="object"==typeof e.attrs?e.attrs:{},e.singleton||"boolean"==typeof e.singleton||(e.singleton=s()),e.insertInto||(e.insertInto="head"),e.insertAt||(e.insertAt="bottom");var n=p(t,e);return f(n,e),function(t){for(var i=[],o=0;o<n.length;o++){var s=n[o];(a=r[s.id]).refs--,i.push(a)}t&&f(p(t,e),e);for(o=0;o<i.length;o++){var a;if(0===(a=i[o]).refs){for(var l=0;l<a.parts.length;l++)a.parts[l]();delete r[a.id]}}}};var x,w=(x=[],function(t,e){return x[t]=e,x.filter(Boolean).join("\n")});function E(t,e,n,i){var o=n?"":i.css;if(t.styleSheet)t.styleSheet.cssText=w(e,o);else{var r=document.createTextNode(o),s=t.childNodes;s[e]&&t.removeChild(s[e]),s.length?t.insertBefore(r,s[e]):t.appendChild(r)}}function _(t,e){var n=e.css,i=e.media;if(i&&t.setAttribute("media",i),t.styleSheet)t.styleSheet.cssText=n;else{for(;t.firstChild;)t.removeChild(t.firstChild);t.appendChild(document.createTextNode(n))}}function P(t,e,n){var i=n.css,o=n.sourceMap,r=void 0===e.convertToAbsoluteUrls&&o;(e.convertToAbsoluteUrls||r)&&(i=d(i)),o&&(i+="\n/*# sourceMappingURL=data:application/json;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(o))))+" */");var s=new Blob([i],{type:"text/css"}),a=t.href;t.href=URL.createObjectURL(s),a&&URL.revokeObjectURL(a)}},function(t,e){t.exports=function(t){var e="undefined"!=typeof window&&window.location;if(!e)throw new Error("fixUrls requires window.location");if(!t||"string"!=typeof t)return t;var n=e.protocol+"//"+e.host,i=n+e.pathname.replace(/\/[^\/]*$/,"/");return t.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi,(function(t,e){var o,r=e.trim().replace(/^"(.*)"$/,(function(t,e){return e})).replace(/^'(.*)'$/,(function(t,e){return e}));return/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/|\s*$)/i.test(r)?t:(o=0===r.indexOf("//")?r:0===r.indexOf("/")?n+r:i+r.replace(/^\.\//,""),"url("+JSON.stringify(o)+")")}))}}])}));