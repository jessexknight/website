/*
 MATLAB Highlighter 1.27, a small and lightweight JavaScript library for colorizing your MATLAB syntax.
 http://matlabtricks.com/matlab-highlighter
 Licensed under the MIT license
 Copyright (c) 2013, Zoltan Fegyver
*/
function highlightMATLABCode(n){function e(i){return(i>="A"&&i<="Z")||(i>="a"&&i<="z")||(i==")")}function l(p,j,i){var q=j.index,r;while(q>=i){r=p.charAt(--q);if(r=="\n"){break}if(r=="'"){continue}else{return !e(r)}}return true}function m(q){var p,r=0,j,s=/(\'[^\'\n]*\')/gi,i=[];while(p=s.exec(q)){if(l(q,p,r)){j=p.index+p[1].length;i.push(q.slice(r,p.index));i.push(q.slice(p.index,j));r=j}}i.push(q.slice(r));return i}function a(s,j){var u='<span class="',t="</span>";if(j){return[u,'string">',s,t].join("")}else{var r=[{r:/\b('|break|case|catch|classdef|continue|else|elseif|end|for|function|global|if|otherwise|parfor|persistent|return|spmd|switch|try|while|')\b/gi,s:"keyword"},{r:/([(){}\[\]\.]+)/gi,s:"bracket"},{r:/\b([0-9]+)\b/gi,s:"number"},{r:/(%[^\n]+)/gi,s:"comment"}];for(var p=0,q=r.length;p<q;p++){s=s.replace(r[p].r,[u,r[p].s,'">$1',t].join(""))}return s}}var c=!!n?[document.getElementById(n)]:document.getElementsByTagName("pre");for(var f=0,o=c.length;f<o;f++){if((" "+c[f].className+" ").indexOf(" matlab-code ")>-1){var b=m(c[f].innerHTML.toString().replace(/<br\s*\/?>/mg,"\n")),g=[],k="&nbsp;";for(var d=0,h=b.length;d<h;d++){g.push(a(b[d],d%2))}c[f].innerHTML=g.join("").replace(/^[ ]/gm,k).replace(/\n/gm,"<br>").replace(/\t/gm,k+k)}}};