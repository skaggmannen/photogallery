function ContentView(aData) {
	var self = this;

	self.ContentState_Loading 	= 0;
	self.ContentState_Gallery 	= 1;
	self.ContentState_Trash		= 2;
	self.ContentState_Image 	= 3;

	self.myState = ko.observable(self.ContentState_Loading);
	self.mySelectedImage = ko.observable();

	self.myGalleryView = new GalleryView(aData);
	self.myTrashView = new TrashView(aData);

	self.showGallery = function showGallery() {
		self.myState(self.ContentState_Gallery);
	};

	self.showTrash = function showTrash() {
		self.myState(self.ContentState_Trash);
	};

	self.showImage = function showImage(aImageId) {
		self.mySelectedImage(aData.getImage(aImageId));
		self.myState(self.ContentState_Image);
	};
};