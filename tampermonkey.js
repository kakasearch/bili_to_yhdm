// ==UserScript==
// @name         b站番剧播放页内跳转樱花搜索
// @namespace    http://tampermonkey.net/
// @version      1.0.3
// @description  打开播放页面发现没会员？点击追番按钮旁边的番剧名跳转至樱花动漫观看
// @author       kakasearch
// @match        https://www.bilibili.com/bangumi/*
// @icon         http://www.yhdm.so/favicon.ico
// run-at        document-end
// ==/UserScript==

(function() {
    'use strict';
    function handle_name(name){
        name = name.replace(/（.*）/,'')//去中文括号
        name = name.replace(/第.*季/,'') //去第二季
        name = name.replace(/剧场版/,'') //去剧场版  "剧场版 王室教师海涅"
        name = name.split('/')[name.split('/').length-1] //去/，保留最后部分
        name = name.slice(0,18)//樱花动漫最长支持18个字符，太长会502
        name = name.trim() // //去多余空格  "无限滑板 / SK8 the Infinity"
        name = name.split(' ')[0] //以空格分割，取前面的   伊甸星原 EDENS ZERO
        name = name.split('，')[name.split('，').length-1] //以，分割，取后面的
        name = name.split('-')[0] // 以-分割，取前面的  "催眠麦克风-Division Rap Battle- Rhyme Anima"
        return name
    }
    function change_url(){
        let a = document.querySelector("#media_module > div > a")
        if(a){
            a.href='http://www.yhdm.so/search/'+ handle_name(a.innerText)+"?bv="+document.querySelector("a.av-link").innerText
            a.style="color:#FF44AA;"
            if (! document.querySelector("#media_module > div > a > img")){
                let img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAqCAMAAAD79pkTAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAPZQTFRFAAAA7GyL7GyL4HuQ526K6Wh/7lt67mF87WWD7mF87WWD6GeD7Vt37lt67myH7mF87mF85WyD7GyL5XqW526K6Wh/7WWD7WWD6WB77mF86Wh/526K5oGW5niO6GeD4Iej5WyD5XOS7mF87mF8526K5X+a6WB75nSL5nSL6WB77WWD5XOS6GeD6GeD7XGN5nSL6GeD7myH6GeD6Wh/7WWD6Wh/7myH6GeD6WB77myH6WB7526K6oOo6WB76GeD5XqW6WB77Hqd7WWD5niO5nSL7XGN7myH6Wh/7myH7mF86WB75nSL5nSL7WWD5XOS526K5WyD5XOSmh+dTAAAAFJ0Uk5TAFVmEVV37syI7ndm//8z/91EMxEiiKqZiJlVMxERRBEzIruqRBHMIjP/ZjNVd3dmiN3du7uZRLvud7t3EZmZIt0R7iIRIlVmZmaqRFXdVYhmRHtUuBsAAAIaSURBVHicpZV9X9MwEMcrsLZZLyQ8rBUKTFseHKLOuTJEBYYiPuDT+38zXtKkTdKO4sf7I7mk3yZ3v1xTz/tve7Qk2uWVB8HLPT8QfUj6D6AjAkARXGWU8rUuep0BpZRseBx7YJsd+IBKixOQfa8Df0wt2+rA+/+Gb9v4QnHSdEd0uwxMfE/MDZ+kDvw0QznyffQykya4xEFIKD08MulnHJ8BjOIN79jEc3EO5YvPa/qkioCnHqmjGa0exFQNyUmFbxINANsf1Hg+DOqdXhh5Ggm+5NrzX1Uu0LEZfB0xkNfqVZgYdGhL86bmmfbqLWFqoLtrvbxayDDjBHhxuqPoGREiOqQzgaOz7K3El6jDoh2es8YcfSfx97yBo2gpceYgUNEEbiREzBbuGrnCnaJVeO7i21qaeCSTrdKDYuitKBdEZtiOCqPEoiTOsumH/nhS6kB42U8utgLiE34+cGsY7TLxqw1UexV53nzeRPErSFoUxRPaa4PLmm+1sIVu6GxY1qDnxArk2hpaFVZqaSs/tY4OILHpj06JjHM7a/bJwm+caD+H9m503V6+PBa9JJvf2jh3Yr8VSzBSPb3RnxKRRxa5uTIa9I7GCkel9R1wnOasrDnLvoiiSBSDd1ak3K94xRUL7u1MRgDf0B1egcYXmlRb/TNOy+jv+0EFPgJn6nqTt6PfVjDavt9d/Li+06Ofs9mv33/uwTvtLyCPR618Lt3pAAAAAElFTkSuQmCC"
                a.innerHTML += `<img src='${img}' style="height: 15px;padding-left: 3px;">`
            }
        }
    }

    let i = setInterval(change_url,100)
    setTimeout(function(){
        clearInterval(i)},5000)

    let ci = 0
    let obser = setInterval(
        function(){
            let video= document.querySelector("#bilibili-player video")
            if(video){
                clearInterval(obser)
                let observer = new MutationObserver(()=>{change_url()})
                observer.observe(video, { attributes: true });//检测video变化,防止中途切p失效
            }

        },200
    )
})();