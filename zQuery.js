
function ZaG(args) {

	return new zQuery(args)
}

function bind(obj,evType,evFn) {

	if(obj.addEventListener){
		obj.addEventListener(evType,evFn,false);
	}else if (obj.attachEvent) {
		obj.attachEvent('on'+evType,evFn);
	}else {
		obj['on'+evType] = evFn;
	}

}

function getStyle(obj,attr) {
	return obj.currentStyle? obj.currentStyle[attr]:getComputedStyle(obj)[attr];
}

function zQuery(args) {

	this.eles = [];

	switch(typeof(args)) {
		case "function":
			bind(window,'DOMContentLoaded',args);
			break;
		case 'string':
			var char = args.charAt(0);
        	if( char == "#") {
                this.eles.push(document.getElementById(args.substring(1)));
            }else if (char == '.') {
            	var allEles = document.getElementsByTagName('*');
                for(var i = 0; i < allEles.length; i++) {
                    var arrClassNames = allEles[i].className.split(' ');

                    for(var k = 0; k < arrClassNames.length; k++) {
                        if(arrClassNames[k] == args.slice(1)){
                            this.eles.push(allEles[i]);
                            break;
                        }
                    }
                }
                
            }else {
                var tags = document.getElementsByTagName(args);
                for(var i = 0; i < tags.length; i++) {
                	this.eles.push(tags[i])
                }
            }
			break;
		case 'object':
			if(args instanceof Array) {
				this.eles = args;
			}else {
				this.eles.push(args);
			}
			
			break;
	}
	return this;
}

zQuery.prototype.css = function (attr,val) {
	
	if(typeof(arguments[0]) == 'object') {

		for(var key_value in arguments[0]) {
			for(var i = 0; i < this.eles.length; i++) {
				
				this.eles[i].style[key_value] = arguments[0][key_value];
			}
		}


	}else {
		
		if(arguments.length == 2) {
			for(var i = 0; i < this.eles.length; i++) {
				this.eles[i].style[attr] = val;
			}
		}else if (arguments.length == 1) {
			// 获取样式
			return getStyle(this.eles[0], attr);
			
		}
	}
	return this;
}

zQuery.prototype.get = function (num) {
	if(!num) {
		return this.eles;
	}
	return this.eles[num];
}

zQuery.prototype.mouseover = function (fn) {
	if(typeof(arguments[0])=='function') {

		for(var i = 0; i < this.eles.length; i++) {
			bind(this.eles[i],'mouseover',fn);
		}
	}
	return this;
}
zQuery.prototype.click = function (fn) {
	if(typeof(arguments[0])=='function') {
		this.on('click', fn);
	}
	return this;
}

zQuery.prototype.on = function (evType,evFn) {
	if(arguments.length == 2) {
		for(var i = 0; i < this.eles.length; i++) {
			bind(this.eles[i], evType, evFn);
		}
	}else {

		for( var k in arguments[0]) {
			for(var i = 0; i < this.eles.length; i++) {
				bind(this.eles[i], k, arguments[0][k]);
			}
		}

	}
	return this;
}

zQuery.prototype.addClass = function(yourClass) {

	for (var i = 0; i < this.eles.length; i++) {


		if(this.eles[i].className==""){
			this.eles[i].className = yourClass
		}else{

			var arrClass = this.eles[i].className.split(" ");

			var _index = arrIndex(arrClass,yourClass)
			if(_index == -1) {
				this.eles[i].className += " "+ yourClass
			}
		}

	}
	return this;
}

function arrIndex(basearrClass, subClass){
	for (var i = 0; i < basearrClass.length; i++) {
		if(basearrClass[i]==subClass) {
			return i
		}
	}
	return -1
}

zQuery.prototype.removeClass = function(yourClass) {

	for (var i = 0; i < this.eles.length; i++) {

		var arrClass = this.eles[i].className.split(" ")

		var _index = arrIndex(arrClass,yourClass)

		if(_index != -1) {
			arrClass.splice(_index,1)
			this.eles[i].className = arrClass.join(" ")
		}
	}

	return this;

}


zQuery.prototype.html = function (htmlStr) {
	if(!arguments.length) {
		return this.eles[0].innerHTML;
	}else {
		for(var i = 0; i < this.eles.length; i++) {
			this.eles[i].innerHTML = htmlStr;
		}
	}
	return this;
}
// 插件机制
ZaG.extend = function (obj) {
	for(var k in obj) {
		ZaG[k] = obj[k]
	}
}

ZaG.fn = zQuery.prototype;

ZaG.fn.extend = function (obj) {
	for(var k in obj) {
		zQuery.prototype[k] = obj[k];
	}
}










