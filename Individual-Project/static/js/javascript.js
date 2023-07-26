document.getElementById("commentlist").style.visibility="hidden";
function view(){
	document.getElementById("commentlist").style.visibility = 'visible';
}
document.getElementById("commentlist").onclick = function() {view()};