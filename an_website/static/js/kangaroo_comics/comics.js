// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-3.0-or-later
export{};function T(){const e=(i,n,a)=>new Date(i,n-1,a,6,0,0,0),h=[[e(2021,5,25),"administratives/kaenguru-comics/25/original/"],[e(2021,9,6),"administratives/kaenguru-comics/2021-09/6/original/"],[e(2021,10,4),"administratives/kaenguru-comics/2021-10/4/original"],[e(2021,10,29),"administratives/kaenguru-comics/29/original"],[e(2021,11,3),"administratives/kaenguru-comics/2021-11/03-11-21/original"],[e(2021,12,6),"administratives/kaenguru-comics/2021-12/6/original"],[e(2022,1,29),"administratives/kaenguru-comics/2022-01/29-3/original"],[e(2022,2,7),"administratives/kaenguru-comics/08-02-22/original"],[e(2022,2,12),"administratives/kaenguru-comics/12/original"],[e(2022,2,14),"administratives/kaenguru-comics/14/original"],[e(2022,3,28),"administratives/kaenguru-comics/2022-03/kaenguru-2022-03-28/original"],[e(2022,4,4),"administratives/kaenguru-comics/2022-04/4/original"],[e(2022,5,9),"administratives/kaenguru-comics/2022-05/9/original"],[e(2022,8,15),"administratives/kaenguru-comics/2022-08/kaenguru-comics-2022-08-15/original"],[e(2022,8,29),"administratives/kaenguru-comics/2022-08/29-3/original"]],D=(i,n,a,t)=>i.getFullYear()===n&&i.getMonth()===a-1&&i.getDate()===t,M=(i,n)=>D(i,n.getFullYear(),n.getMonth()+1,n.getDate()),m=i=>i&&i.getDay()===0&&!D(i,2020,12,20),f=i=>e(i.getFullYear(),i.getMonth()+1,i.getDate()),y=()=>f(new Date),o=[],B=`/static/img/2020-11-03.jpg
administratives/kaenguru-comics/pilot-kaenguru/original
administratives/kaenguru-comics/pow-kaenguru/original
static/img/kaenguru-announcement/original
administratives/kaenguru-comics/der-baum-kaenguru/original
administratives/kaenguru-comics/warnung-kaenguru/original
administratives/kaenguru-comics/kaenguru-005/original
administratives/kaenguru-comics/kaenguru-006/original
administratives/kaenguru-comics/kaenguru-007/original
administratives/kaenguru-comics/kaenguru-008/original
administratives/kaenguru-comics/kaenguru-009/original
administratives/kaenguru-comics/kaenguru-010/original
administratives/kaenguru-comics/kaenguru-011/original
administratives/kaenguru-comics/kaenguru-012/original
administratives/kaenguru-comics/kaenguru-013/original
administratives/kaenguru-comics/kaenguru-014/original
administratives/kaenguru-comics/kaenguru-015/original
administratives/kaenguru-comics/kaenguru-016/original
administratives/kaenguru-comics/kaenguru-017/original
administratives/kaenguru-comics/kaenguru-018/original
administratives/2020-12/kaenguru-comics-kaenguru-019/original
administratives/kaenguru-comics/kaenguru-020/original
administratives/kaenguru-comics/kaenguru-021/original
administratives/kaenguru-comics/kaenguru-023/original
administratives/kaenguru-comics/kaenguru-024/original
administratives/kaenguru-comics/kaenguru-025/original
administratives/kaenguru-comics/kaenguru-026/original
administratives/kaenguru-comics/kaenguru-027/original
administratives/kaenguru-comics/kaenguru-028/original
administratives/kaenguru-comics/kaenguru-029/original
administratives/kaenguru-comics/kaenguru-030/original
administratives/kaenguru-comics/kaenguru-031/original
administratives/kaenguru-comics/kaenguru-032/original
administratives/kaenguru-comics/kaenguru-033/original
administratives/kaenguru-comics/kaenguru-034/original
administratives/kaenguru-comics/kaenguru-035/original
administratives/kaenguru-comics/kaenguru-036/original
administratives/kaenguru-comics/kaenguru-037/original
administratives/kaenguru-comics/kaenguru-038-2/original
administratives/kaenguru-comics/kaenguru-039/original
administratives/kaenguru-comics/kaenguru-040/original
administratives/kaenguru-comics/kaenguru-41/original
administratives/kaenguru-comics/kaenguru-42/original
administratives/kaenguru-comics/kaenguru-43/original
administratives/kaenguru-comics/kaenguru-44/original
administratives/kaenguru-comics/kaenguru-045/original
`;function F(){const i=y(),n=f(A);for(;n.getTime()<=i.getTime();)o.push(C(n)),u(n,1)}const N=["Sonntag","Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag"],S=i=>N[i.getDay()],x=["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],H=i=>x[i.getMonth()],l=i=>`Comic von ${S(i)}, dem ${i.getDate()}. ${H(i)} ${i.getFullYear()}`;function d(){for(const i of document.getElementsByClassName("popup-container"))i.remove()}const L=document.getElementById("current-comic-header"),k=document.getElementById("current-img");k.onmouseover=d;function b(i){let n=C(i);n=n.startsWith("/")?n:"https://img.zeit.de/"+n,k.src=n,L.innerText="Neuster "+l(i)+":",L.href=n}const z=e(2020,12,3),Y=/administratives\/kaenguru-comics\/kaenguru-(\d{2,3})(?:-2)?\/original\/?/,A=e(2021,1,19),W=/administratives\/kaenguru-comics\/(\d{4})-(\d{2})\/(\d{2})\/original\/?/,$=/\/static\/img\/(\d{4})-(\d{1,2})-(\d{1,2})\.jpg/;function J(i){for(const a of[W,$]){const t=i.toLowerCase().match(a);if(t&&t.length>3)return e(parseInt(t[1]),parseInt(t[2]),parseInt(t[3]))}const n=i.toLowerCase().match(Y);if(n&&n.length>1){const a=parseInt(n[1])-5,t=new Date(z.getTime());for(let r=0;r<a;r++)t.setTime(u(t,m(t)?2:1).getTime());return m(t)?u(t,1):t}switch(i=i.toLowerCase().trim(),i){case"administratives/kaenguru-comics/pilot-kaenguru/original":return e(2020,11,29);case"administratives/kaenguru-comics/pow-kaenguru/original":return e(2020,11,30);case"static/img/kaenguru-announcement/original":return e(2020,11,30);case"administratives/kaenguru-comics/der-baum-kaenguru/original":return e(2020,12,1);case"administratives/kaenguru-comics/warnung-kaenguru/original":return e(2020,12,2);case"administratives/2020-12/kaenguru-comics-kaenguru-019/original":return e(2020,12,19)}for(const a of h)if(i===a[1])return a[0];return null}const O="administratives/kaenguru-comics/%y-%m/%d/original";function C(i){for(const t of h)if(M(i,t[0]))return t[1];const n=(i.getMonth()+1).toString(),a=i.getDate().toString();return O.replace("%y",i.getFullYear().toString()).replace("%m",n.length===2?n:"0"+n).replace("%d",a.length===2?a:"0"+a)}function u(i,n){return i.setTime(i.getTime()+n*1e3*60*60*24),i.setHours(6),i}const E=7,I=document.getElementById("load-button"),w=document.getElementById("old-comics-list");let g=0;const R=()=>{for(let i=0;i<E;i++){g++;const n=o.length-g;if(n<0)break;let a=o[n];const t=J(a);if(t===null){console.error("No date found for "+a);continue}a=a.startsWith("/")?a:"https://img.zeit.de/"+a;const r=document.createElement("li"),c=document.createElement("a");c.classList.add("comic-header"),c.innerText=l(t)+":",c.href=a,c.style.fontSize="25px",r.appendChild(c),r.appendChild(document.createElement("br"));const s=document.createElement("img");s.classList.add("normal-img"),s.src=a,s.alt=l(t),s.onclick=()=>{j(s)},s.onerror=()=>{m(t)?w.removeChild(r):r.append(" konnte nicht geladen werden.")},r.appendChild(s),w.appendChild(r)}g>=o.length&&(I.style.opacity="0",I.style.visibility="invisible")};document.getElementById("load-button").onclick=R;const j=i=>{d();const n=document.createElement("div");n.classList.add("popup-container"),n.onmouseleave=()=>{n.remove()},n.onclick=()=>{d()};const a=i.cloneNode(!0);a.classList.remove("normal-img"),a.classList.add("popup-img");const t=document.createElement("img");t.classList.add("close-button"),t.src="/static/img/close.svg?v=0",n.appendChild(a),n.appendChild(t),i.parentNode.appendChild(n)};o.concat(B.split(`
`)),F();const v=u(y(),1);b(v),k.onerror=()=>{u(v,-1),b(v),g<E&&g++}}const p=document.getElementById("start-button-no_3rd_party");if(p!==null){const e=document.getElementById("comic-content-container");p.onclick=()=>{p.remove(),e.classList.remove("hidden"),T()},e.classList.add("hidden")}else T();// @license-end
//# sourceMappingURL=comics.js.map
