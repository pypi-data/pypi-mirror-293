!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.download=t():(e.xgplayer=e.xgplayer||{},e.xgplayer.PlayerControls=e.xgplayer.PlayerControls||{},e.xgplayer.PlayerControls.download=t())}(window,(function(){return function(e){var t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(r,o,function(t){return e[t]}.bind(null,o));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=0)}([function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=a(n(1)),o=a(n(4));function a(e){return e&&e.__esModule?e:{default:e}}t.default={name:"download",method:function(){r.default.method.call(this),o.default.method.call(this)}},e.exports=t.default},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r,o=n(2),a=(r=o)&&r.__esModule?r:{default:r},i=n(3);t.default={name:"download",method:function(){var e=this;function t(){e.download()}e.on("downloadBtnClick",t),e.once("destroy",(function n(){e.off("downloadBtnClick",t),e.off("destroy",n)})),e.download=function(){var e=(0,i.getAbsoluteURL)(this.config.url);(0,a.default)(e)}}},e.exports=t.default},function(e,t,n){var r,o,a;o=[],void 0===(a="function"==typeof(r=function(){return function e(t,n,r){var o,a,i=window,s="application/octet-stream",l=r||s,c=t,u=!n&&!r&&c,f=document.createElement("a"),d=function(e){return String(e)},p=i.Blob||i.MozBlob||i.WebKitBlob||d,g=n||"download";if(p=p.call?p.bind(i):Blob,"true"===String(this)&&(l=(c=[c,l])[0],c=c[1]),u&&u.length<2048&&(g=u.split("/").pop().split("?")[0],f.href=u,-1!==f.href.indexOf(u))){var h=new XMLHttpRequest;return h.open("GET",u,!0),h.responseType="blob",h.onload=function(t){e(t.target.response,g,s)},setTimeout((function(){h.send()}),0),h}if(/^data:([\w+-]+\/[\w+.-]+)?[,;]/.test(c)){if(!(c.length>2096103.424&&p!==d))return navigator.msSaveBlob?navigator.msSaveBlob(b(c),g):w(c);l=(c=b(c)).type||s}else if(/([\x80-\xff])/.test(c)){for(var v=0,y=new Uint8Array(c.length),m=y.length;v<m;++v)y[v]=c.charCodeAt(v);c=new p([y],{type:l})}function b(e){for(var t=e.split(/[:;,]/),n=t[1],r=("base64"==t[2]?atob:decodeURIComponent)(t.pop()),o=r.length,a=0,i=new Uint8Array(o);a<o;++a)i[a]=r.charCodeAt(a);return new p([i],{type:n})}function w(e,t){if("download"in f)return f.href=e,f.setAttribute("download",g),f.className="download-js-link",f.innerHTML="downloading...",f.style.display="none",document.body.appendChild(f),setTimeout((function(){f.click(),document.body.removeChild(f),!0===t&&setTimeout((function(){i.URL.revokeObjectURL(f.href)}),250)}),66),!0;if(/(Version)\/(\d+)\.(\d+)(?:\.(\d+))?.*Safari\//.test(navigator.userAgent))return/^data:/.test(e)&&(e="data:"+e.replace(/^data:([\w\/\-\+]+)/,s)),window.open(e)||confirm("Displaying New Document\n\nUse Save As... to download, then click back to return to this page.")&&(location.href=e),!0;var n=document.createElement("iframe");document.body.appendChild(n),!t&&/^data:/.test(e)&&(e="data:"+e.replace(/^data:([\w\/\-\+]+)/,s)),n.src=e,setTimeout((function(){document.body.removeChild(n)}),333)}if(o=c instanceof p?c:new p([c],{type:l}),navigator.msSaveBlob)return navigator.msSaveBlob(o,g);if(i.URL)w(i.URL.createObjectURL(o),!0);else{if("string"==typeof o||o.constructor===d)try{return w("data:"+l+";base64,"+i.btoa(o))}catch(e){return w("data:"+l+","+encodeURIComponent(o))}(a=new FileReader).onload=function(e){w(this.result)},a.readAsDataURL(o)}return!0}})?r.apply(t,o):r)||(e.exports=a)},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});t.getAbsoluteURL=function(e){if(!e.match(/^https?:\/\//)){var t=document.createElement("div");t.innerHTML='<a href="'+e+'">x</a>',e=t.firstChild.href}return e}},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r,o=n(5),a=n(7),i=(r=a)&&r.__esModule?r:{default:r};n(8);t.default={name:"s_download",method:function(){var e=this;if(e.config.download){var t=(0,o.createDom)("xg-download",'<xg-icon class="xgplayer-icon">'+i.default+"</xg-icon>",{},"xgplayer-download"),n=e.lang.DOWNLOAD_TIPS,r=(0,o.createDom)("xg-tips",'<span class="xgplayer-tip-download">'+n+"</span>",{},"xgplayer-tips");t.appendChild(r),e.once("ready",(function(){e.controls.appendChild(t)})),["click","touchend"].forEach((function(n){t.addEventListener(n,(function(t){t.preventDefault(),t.stopPropagation(),e.userGestureTrigEvent("downloadBtnClick")}))}))}}},e.exports=t.default},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.util=t.PresentationMode=void 0,t.createDom=i,t.hasClass=s,t.addClass=l,t.removeClass=c,t.toggleClass=u,t.findDom=f,t.padStart=d,t.format=p,t.event=g,t.typeOf=h,t.deepCopy=v,t.getBgImage=y,t.copyDom=m,t._setInterval=b,t._clearInterval=w,t.createImgBtn=x,t.isWeiXin=L,t.isUc=C,t.computeWatchDur=O,t.offInDestroy=k,t.on=j,t.once=M,t.getBuffered2=S,t.checkIsBrowser=E,t.setStyle=U,t.checkWebkitSetPresentationMode=function(e){return"function"==typeof e.webkitSetPresentationMode};var r,o=n(6),a=(r=o)&&r.__esModule?r:{default:r};function i(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"div",t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"",n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"",o=document.createElement(e);return o.className=r,o.innerHTML=t,Object.keys(n).forEach((function(t){var r=t,a=n[t];"video"===e||"audio"===e?a&&o.setAttribute(r,a):o.setAttribute(r,a)})),o}function s(e,t){return!!e&&(e.classList?Array.prototype.some.call(e.classList,(function(e){return e===t})):!!e.className&&!!e.className.match(new RegExp("(\\s|^)"+t+"(\\s|$)")))}function l(e,t){e&&(e.classList?t.replace(/(^\s+|\s+$)/g,"").split(/\s+/g).forEach((function(t){t&&e.classList.add(t)})):s(e,t)||(e.className+=" "+t))}function c(e,t){e&&(e.classList?t.split(/\s+/g).forEach((function(t){e.classList.remove(t)})):s(e,t)&&t.split(/\s+/g).forEach((function(t){var n=new RegExp("(\\s|^)"+t+"(\\s|$)");e.className=e.className.replace(n," ")})))}function u(e,t){e&&t.split(/\s+/g).forEach((function(t){s(e,t)?c(e,t):l(e,t)}))}function f(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:document,t=arguments[1],n=void 0;try{n=e.querySelector(t)}catch(r){0===t.indexOf("#")&&(n=e.getElementById(t.slice(1)))}return n}function d(e,t,n){for(var r=String(n),o=t>>0,a=Math.ceil(o/r.length),i=[],s=String(e);a--;)i.push(r);return i.join("").substring(0,o-s.length)+s}function p(e){if(window.isNaN(e))return"";var t=d(Math.floor(e/3600),2,0),n=d(Math.floor((e-3600*t)/60),2,0),r=d(Math.floor(e-3600*t-60*n),2,0);return("00"===t?[n,r]:[t,n,r]).join(":")}function g(e){if(e.touches){var t=e.touches[0]||e.changedTouches[0];e.clientX=t.clientX||0,e.clientY=t.clientY||0,e.offsetX=t.pageX-t.target.offsetLeft,e.offsetY=t.pageY-t.target.offsetTop}e._target=e.target||e.srcElement}function h(e){return Object.prototype.toString.call(e).match(/([^\s.*]+)(?=]$)/g)[0]}function v(e,t){if("Object"===h(t)&&"Object"===h(e))return Object.keys(t).forEach((function(n){"Object"!==h(t[n])||t[n]instanceof Node?"Array"===h(t[n])?e[n]="Array"===h(e[n])?e[n].concat(t[n]):t[n]:e[n]=t[n]:e[n]?v(e[n],t[n]):e[n]=t[n]})),e}function y(e){var t=(e.currentStyle||window.getComputedStyle(e,null)).backgroundImage;if(!t||"none"===t)return"";var n=document.createElement("a");return n.href=t.replace(/url\("|"\)/g,""),n.href}function m(e){if(e&&1===e.nodeType){var t=document.createElement(e.tagName);return Array.prototype.forEach.call(e.attributes,(function(e){t.setAttribute(e.name,e.value)})),e.innerHTML&&(t.innerHTML=e.innerHTML),t}return""}function b(e,t,n,r){e._interval[t]||(e._interval[t]=setInterval(n.bind(e),r))}function w(e,t){clearInterval(e._interval[t]),e._interval[t]=null}function x(e,t,n,r){var o=i("xg-"+e,"",{},"xgplayer-"+e+"-img");if(o.style.backgroundImage='url("'+t+'")',n&&r){var a=void 0,s=void 0,l=void 0;["px","rem","em","pt","dp","vw","vh","vm","%"].every((function(e){return!(n.indexOf(e)>-1&&r.indexOf(e)>-1)||(a=Number(n.slice(0,n.indexOf(e)).trim()),s=Number(r.slice(0,r.indexOf(e)).trim()),l=e,!1)})),o.style.width=""+a+l,o.style.height=""+s+l,o.style.backgroundSize=""+a+l+" "+s+l,o.style.margin="start"===e?"-"+s/2+l+" auto auto -"+a/2+l:"auto 5px auto 5px"}return o}function L(){return window.navigator.userAgent.toLowerCase().indexOf("micromessenger")>-1}function C(){return window.navigator.userAgent.toLowerCase().indexOf("ucbrowser")>-1}function O(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],t=[],n=0;n<e.length;n++)if(!(!e[n].end||e[n].begin<0||e[n].end<0||e[n].end<e[n].begin))if(t.length<1)t.push({begin:e[n].begin,end:e[n].end});else for(var r=0;r<t.length;r++){var o=e[n].begin,a=e[n].end;if(a<t[r].begin){t.splice(r,0,{begin:o,end:a});break}if(!(o>t[r].end)){var i=t[r].begin,s=t[r].end;t[r].begin=Math.min(o,i),t[r].end=Math.max(a,s);break}if(r>t.length-2){t.push({begin:o,end:a});break}}for(var l=0,c=0;c<t.length;c++)l+=t[c].end-t[c].begin;return l}function k(e,t,n,r){e.once(r,(function o(){e.off(t,n),e.off(r,o)}))}function j(e,t,n,r){if(r)e.on(t,n),k(e,t,n,r);else{e.on(t,(function r(o){n(o),e.off(t,r)}))}}function M(e,t,n,r){if(r)e.once(t,n),k(e,t,n,r);else{e.once(t,(function r(o){n(o),e.off(t,r)}))}}function S(e){for(var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:.5,n=[],r=0;r<e.length;r++)n.push({start:e.start(r)<.5?0:e.start(r),end:e.end(r)});n.sort((function(e,t){var n=e.start-t.start;return n||t.end-e.end}));var o=[];if(t)for(var i=0;i<n.length;i++){var s=o.length;if(s){var l=o[s-1].end;n[i].start-l<t?n[i].end>l&&(o[s-1].end=n[i].end):o.push(n[i])}else o.push(n[i])}else o=n;return new a.default(o)}function E(){return!("undefined"==typeof window||void 0===window.document||void 0===window.document.createElement)}function U(e,t,n){var r=e.style;try{r[t]=n}catch(e){r.setProperty(t,n)}}t.PresentationMode={PIP:"picture-in-picture",INLINE:"inline",FULLSCREEN:"fullscreen"};t.util={createDom:i,hasClass:s,addClass:l,removeClass:c,toggleClass:u,findDom:f,padStart:d,format:p,event:g,typeOf:h,deepCopy:v,getBgImage:y,copyDom:m,setInterval:b,clearInterval:w,createImgBtn:x,isWeiXin:L,isUc:C,computeWatchDur:O,offInDestroy:k,on:j,once:M,getBuffered2:S,checkIsBrowser:E,setStyle:U}},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}();var o=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.bufferedList=t}return r(e,[{key:"start",value:function(e){return this.bufferedList[e].start}},{key:"end",value:function(e){return this.bufferedList[e].end}},{key:"length",get:function(){return this.bufferedList.length}}]),e}();t.default=o,e.exports=t.default},function(e,t,n){"use strict";n.r(t),t.default='<svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" viewBox="0 0 24 24">\n  <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\n    <g transform="translate(-488.000000, -340.000000)" fill="#FFFFFF">\n      <g id="Group-2">\n        <g id="volme_big-copy" transform="translate(488.000000, 340.000000)">\n          <rect id="Rectangle-18" x="11" y="4" width="2" height="12" rx="1"></rect>\n          <rect id="Rectangle-2" x="3" y="18" width="18" height="2" rx="1"></rect>\n          <rect id="Rectangle-2" transform="translate(4.000000, 17.500000) rotate(90.000000) translate(-4.000000, -17.500000) " x="1.5" y="16.5" width="5" height="2" rx="1"></rect><rect id="Rectangle-2-Copy-3" transform="translate(20.000000, 17.500000) rotate(90.000000) translate(-20.000000, -17.500000) " x="17.5" y="16.5" width="5" height="2" rx="1"></rect>\n          <path d="M9.48791171,8.26502656 L9.48791171,14.2650266 C9.48791171,14.8173113 9.04019646,15.2650266 8.48791171,15.2650266 C7.93562696,15.2650266 7.48791171,14.8173113 7.48791171,14.2650266 L7.48791171,7.26502656 C7.48791171,6.71274181 7.93562696,6.26502656 8.48791171,6.26502656 L15.4879117,6.26502656 C16.0401965,6.26502656 16.4879117,6.71274181 16.4879117,7.26502656 C16.4879117,7.81731131 16.0401965,8.26502656 15.4879117,8.26502656 L9.48791171,8.26502656 Z" id="Combined-Shape" transform="translate(11.987912, 10.765027) scale(1, -1) rotate(45.000000) translate(-11.987912, -10.765027) "></path>\n        </g>\n      </g>\n    </g>\n  </g>\n</svg>\n'},function(e,t,n){var r=n(9);"string"==typeof r&&(r=[[e.i,r,""]]);var o={hmr:!0,transform:void 0,insertInto:void 0};n(11)(r,o);r.locals&&(e.exports=r.locals)},function(e,t,n){(e.exports=n(10)(!1)).push([e.i,".xgplayer-skin-default .xgplayer-download{position:relative;-webkit-order:9;-moz-box-ordinal-group:10;order:9;display:block;cursor:pointer}.xgplayer-skin-default .xgplayer-download .xgplayer-icon{margin-top:3px}.xgplayer-skin-default .xgplayer-download .xgplayer-icon div{position:absolute}.xgplayer-skin-default .xgplayer-download .xgplayer-icon svg{position:relative;top:5px;left:5px}.xgplayer-skin-default .xgplayer-download .xgplayer-tips{margin-left:-20px}.xgplayer-skin-default .xgplayer-download .xgplayer-tips .xgplayer-tip-download{display:block}.xgplayer-skin-default .xgplayer-download:hover{opacity:.85}.xgplayer-skin-default .xgplayer-download:hover .xgplayer-tips{display:block}.xgplayer-lang-is-en .xgplayer-download .xgplayer-tips{margin-left:-32px}.xgplayer-lang-is-jp .xgplayer-download .xgplayer-tips{margin-left:-40px}",""])},function(e,t){e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var n=function(e,t){var n=e[1]||"",r=e[3];if(!r)return n;if(t&&"function"==typeof btoa){var o=(i=r,"/*# sourceMappingURL=data:application/json;charset=utf-8;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(i))))+" */"),a=r.sources.map((function(e){return"/*# sourceURL="+r.sourceRoot+e+" */"}));return[n].concat(a).concat([o]).join("\n")}var i;return[n].join("\n")}(t,e);return t[2]?"@media "+t[2]+"{"+n+"}":n})).join("")},t.i=function(e,n){"string"==typeof e&&(e=[[null,e,""]]);for(var r={},o=0;o<this.length;o++){var a=this[o][0];"number"==typeof a&&(r[a]=!0)}for(o=0;o<e.length;o++){var i=e[o];"number"==typeof i[0]&&r[i[0]]||(n&&!i[2]?i[2]=n:n&&(i[2]="("+i[2]+") and ("+n+")"),t.push(i))}},t}},function(e,t,n){var r,o,a={},i=(r=function(){return window&&document&&document.all&&!window.atob},function(){return void 0===o&&(o=r.apply(this,arguments)),o}),s=function(e){return document.querySelector(e)},l=function(e){var t={};return function(e){if("function"==typeof e)return e();if(void 0===t[e]){var n=s.call(this,e);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}t[e]=n}return t[e]}}(),c=null,u=0,f=[],d=n(12);function p(e,t){for(var n=0;n<e.length;n++){var r=e[n],o=a[r.id];if(o){o.refs++;for(var i=0;i<o.parts.length;i++)o.parts[i](r.parts[i]);for(;i<r.parts.length;i++)o.parts.push(b(r.parts[i],t))}else{var s=[];for(i=0;i<r.parts.length;i++)s.push(b(r.parts[i],t));a[r.id]={id:r.id,refs:1,parts:s}}}}function g(e,t){for(var n=[],r={},o=0;o<e.length;o++){var a=e[o],i=t.base?a[0]+t.base:a[0],s={css:a[1],media:a[2],sourceMap:a[3]};r[i]?r[i].parts.push(s):n.push(r[i]={id:i,parts:[s]})}return n}function h(e,t){var n=l(e.insertInto);if(!n)throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");var r=f[f.length-1];if("top"===e.insertAt)r?r.nextSibling?n.insertBefore(t,r.nextSibling):n.appendChild(t):n.insertBefore(t,n.firstChild),f.push(t);else if("bottom"===e.insertAt)n.appendChild(t);else{if("object"!=typeof e.insertAt||!e.insertAt.before)throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");var o=l(e.insertInto+" "+e.insertAt.before);n.insertBefore(t,o)}}function v(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e);var t=f.indexOf(e);t>=0&&f.splice(t,1)}function y(e){var t=document.createElement("style");return e.attrs.type="text/css",m(t,e.attrs),h(e,t),t}function m(e,t){Object.keys(t).forEach((function(n){e.setAttribute(n,t[n])}))}function b(e,t){var n,r,o,a;if(t.transform&&e.css){if(!(a=t.transform(e.css)))return function(){};e.css=a}if(t.singleton){var i=u++;n=c||(c=y(t)),r=L.bind(null,n,i,!1),o=L.bind(null,n,i,!0)}else e.sourceMap&&"function"==typeof URL&&"function"==typeof URL.createObjectURL&&"function"==typeof URL.revokeObjectURL&&"function"==typeof Blob&&"function"==typeof btoa?(n=function(e){var t=document.createElement("link");return e.attrs.type="text/css",e.attrs.rel="stylesheet",m(t,e.attrs),h(e,t),t}(t),r=O.bind(null,n,t),o=function(){v(n),n.href&&URL.revokeObjectURL(n.href)}):(n=y(t),r=C.bind(null,n),o=function(){v(n)});return r(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap)return;r(e=t)}else o()}}e.exports=function(e,t){if("undefined"!=typeof DEBUG&&DEBUG&&"object"!=typeof document)throw new Error("The style-loader cannot be used in a non-browser environment");(t=t||{}).attrs="object"==typeof t.attrs?t.attrs:{},t.singleton||"boolean"==typeof t.singleton||(t.singleton=i()),t.insertInto||(t.insertInto="head"),t.insertAt||(t.insertAt="bottom");var n=g(e,t);return p(n,t),function(e){for(var r=[],o=0;o<n.length;o++){var i=n[o];(s=a[i.id]).refs--,r.push(s)}e&&p(g(e,t),t);for(o=0;o<r.length;o++){var s;if(0===(s=r[o]).refs){for(var l=0;l<s.parts.length;l++)s.parts[l]();delete a[s.id]}}}};var w,x=(w=[],function(e,t){return w[e]=t,w.filter(Boolean).join("\n")});function L(e,t,n,r){var o=n?"":r.css;if(e.styleSheet)e.styleSheet.cssText=x(t,o);else{var a=document.createTextNode(o),i=e.childNodes;i[t]&&e.removeChild(i[t]),i.length?e.insertBefore(a,i[t]):e.appendChild(a)}}function C(e,t){var n=t.css,r=t.media;if(r&&e.setAttribute("media",r),e.styleSheet)e.styleSheet.cssText=n;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(n))}}function O(e,t,n){var r=n.css,o=n.sourceMap,a=void 0===t.convertToAbsoluteUrls&&o;(t.convertToAbsoluteUrls||a)&&(r=d(r)),o&&(r+="\n/*# sourceMappingURL=data:application/json;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(o))))+" */");var i=new Blob([r],{type:"text/css"}),s=e.href;e.href=URL.createObjectURL(i),s&&URL.revokeObjectURL(s)}},function(e,t){e.exports=function(e){var t="undefined"!=typeof window&&window.location;if(!t)throw new Error("fixUrls requires window.location");if(!e||"string"!=typeof e)return e;var n=t.protocol+"//"+t.host,r=n+t.pathname.replace(/\/[^\/]*$/,"/");return e.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi,(function(e,t){var o,a=t.trim().replace(/^"(.*)"$/,(function(e,t){return t})).replace(/^'(.*)'$/,(function(e,t){return t}));return/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/|\s*$)/i.test(a)?e:(o=0===a.indexOf("//")?a:0===a.indexOf("/")?n+a:r+a.replace(/^\.\//,""),"url("+JSON.stringify(o)+")")}))}}])}));