var nodeVersions = [
    "10.6.0",
    "10.5.0",
    "10.4.1",
    "10.4.0",
    "10.3.0",
    "10.2.1",
    "10.2.0",
    "10.1.0",
    "10.0.0",
    "9.11.2",
    "9.11.1",
    "9.11.0",
    "9.10.1",
    "9.10.0",
    "9.9.0",
    "9.8.0",
    "9.7.1",
    "9.7.0",
    "9.6.1",
    "9.6.0",
    "9.5.0",
    "9.4.0",
    "9.3.0",
    "9.2.1",
    "9.2.0",
    "9.1.0",
    "9.0.0",
    "8.11.3",
    "8.11.2",
    "8.11.1",
    "8.11.0",
    "8.10.0",
    "8.9.4",
    "8.9.3",
    "8.9.2",
    "8.9.1",
    "8.9.0",
    "8.8.1",
    "8.8.0",
    "8.7.0",
    "8.6.0",
    "8.5.0",
    "8.4.0",
    "8.3.0",
    "8.2.1",
    "8.2.0",
    "8.1.4",
    "8.1.3",
    "8.1.2",
    "8.1.1",
    "8.1.0",
    "8.0.0"]

var nodeVersionIndex = 0;

function doEvent( obj, event ) {
    var event = new Event( event, {target: obj, bubbles: true} );
    return obj ? obj.dispatchEvent(event) : false;
}

function pressPlusButton(count, callback) {
	if (count == 0) {
		callback();
		return;
	}

	document.querySelector("i.fa.fa-plus").click();

	setTimeout(() => pressPlusButton(--count, callback), 200);
}

function addNodeVersion(nodeVersion, rowIndex) {
	console.log(rowIndex)
	var row = document.querySelectorAll('div.Row__flexRow___3KPUM');
	row = row[rowIndex];

	var inputs = row.querySelectorAll('input.SimpleInput__default___gdtxe');

	inputs[0].value = 'master';
	inputs[1].value = '/version/' + nodeVersion + '/Dockerfile';
	inputs[2].value = nodeVersion;

	doEvent(inputs[0], 'input');
	doEvent(inputs[1], 'input');
	doEvent(inputs[2], 'input');
}

var startingRowCount = document.querySelectorAll('div.Row__flexRow___3KPUM').length;

pressPlusButton(nodeVersions.length, () => {
	console.log('call')
	var i = 0;
	for (var nodeVersion of nodeVersions) {
		addNodeVersion(nodeVersion, i + startingRowCount);
		i=i+1;
	}
});



