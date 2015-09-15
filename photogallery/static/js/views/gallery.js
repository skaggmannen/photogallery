function GalleryView(aData) {
	var self = this;

	self.myData = aData;

	self.select = function select(aImage) {
		if (aImage.myId() === undefined)
		{
			return;
		}
		
		var hash = "#/image/" + aImage.myId();

		if (window.location.hash == hash) {
			return;
		}

		window.location.hash = hash;
	};
};