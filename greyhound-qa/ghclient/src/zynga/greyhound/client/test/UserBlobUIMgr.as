package zynga.greyhound.client.test
{
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.display.Sprite;
	import flash.display.Stage;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.net.URLRequest;
	import flash.system.LoaderContext;
	import flash.system.Security;
	import flash.utils.ByteArray;
	import flash.utils.describeType;
	
	import mx.collections.ArrayCollection;
	import mx.controls.Alert;
	import mx.utils.ObjectUtil;
	
	import spark.components.Button;
	
	import zynga.greyhound.client.base.Constants;
	import zynga.greyhound.client.base.ErrorCodes;
	import zynga.greyhound.client.base.IGame;
	import zynga.greyhound.client.base.IGreyhound;
	import zynga.greyhound.client.base.IStorage;
	import zynga.greyhound.client.base.ITime;
	
	public class UserBlobUIMgr
	{
		private var m_ui:Object;
		private var m_storage:Storage;
		private var m_greyhound:IGreyhound;
		
		private var auto_blobType:String = "player";
		private var auto_new_cas:String = null;
		public var auto_arr_blb:ArrayCollection = new ArrayCollection();
		private var auto_obj:Object;
		private var auto_zid:String = "1";
		
		public function UserBlobUIMgr(greyhound:IGreyhound, uiControls:Object = null)
		{
			m_greyhound = greyhound;
			m_ui = uiControls;
			m_storage = new Storage(m_greyhound);
			if (m_ui != null)	
				initHandlers();
		}
		
		public function removeHandlers():void
		{
			m_ui.whoseBlobSel.removeEventListener(Event.CLOSE, BlobSelhand);
			
			m_ui.getBlobBtn.removeEventListener(MouseEvent.CLICK, getBlobBtnhand);
			
			m_ui.onlineOrOffline.removeEventListener(MouseEvent.CLICK, onlineOrOfflinehand);
			
			m_ui.setBlobBtn.removeEventListener(MouseEvent.CLICK, setBlobBtnhand);
			m_greyhound = null;
			m_ui = null;
			m_storage = null;
		}
		
		public function auto_updateBlobField(blobType : String,status : Object, params : Object) : void
		{
			auto_obj = new Object();
			if(status.error === ErrorCodes.SUCCESS )
			{	if( params.blobs[blobType] && params.blobs[blobType].error === ErrorCodes.SUCCESS) 
			{
				var oData:Object = params.blobs[blobType];
				var oBlob:Object = oData.value.readUTFBytes(oData.value.length);
				auto_new_cas = oData.cas;
				auto_obj["Result"] = "PASS";
				auto_obj["Error Code"] = oData.error;
			}
			else
			{
				auto_obj["Result"] = "FAIL";
				auto_obj["Error Code"] = "404";
			}
			} 
			else 
			{
				auto_obj["Result"] = "FAIL";
				auto_obj["Error Code"] = status.error;
			}
			
			auto_obj["API"] = "user.blob.get";
			auto_arr_blb.addItem(auto_obj);			
		}
		
		public function auto_updateFriendBlobField(blobType : String,status : Object, params : Object) : void
		{
			auto_obj = new Object();
			if(status.error === ErrorCodes.SUCCESS)
			{
				if( params.blobs[blobType] && params.blobs[blobType].error === ErrorCodes.SUCCESS) 
				{
					var oData:Object = params.blobs[blobType];
					var oBlob:Object = oData.value.readUTFBytes(oData.value.length);
					//new_cas = oData.cas;
					auto_obj["Result"] = "PASS";
					auto_obj["Error Code"] = oData.error;
				}
				else
				{
					auto_obj["Error Code"] = "404";
					auto_obj["Result"] = "FAIL";
				}
			} 
			else 
			{
				auto_obj["Error Code"] = status.error;
				auto_obj["Result"] = "FAIL";
			}
			
			auto_obj["API"] = "friend.blob.get";
			auto_arr_blb.addItem(auto_obj);			
		}
		
		public function updateBlobField(blobType : String,status : Object, params : Object) : void
		{
			if(status.error === ErrorCodes.SUCCESS && params.blobs[blobType] && params.blobs[blobType].error === ErrorCodes.SUCCESS) {
				var oData:Object = params.blobs[blobType];
				var oBlob:Object = oData.value.readUTFBytes(oData.value.length);
				m_ui.displayCAS.text = oData.cas;
				m_ui.displayBlob.text = JSON.stringify(oBlob);
			} else {
				m_ui.displayBlob.text = "Failed to get data";
			}
		}
		
		public function auto_updateBlobStatus(status : Object, params : Object):void
		{
			auto_obj = new Object();
			if(status.error === ErrorCodes.SUCCESS) 
			{
				auto_obj["Result"] = "PASS";		
			} 
			else 
			{
				auto_obj["Result"] = "FAIL";
			}
			
			auto_obj["API"] = "user.blob.set";
			auto_obj["Error Code"] = status.error;
			auto_arr_blb.addItem(auto_obj);
		}
		
		public function updateBlobStatus(status : Object, params : Object):void
		{
			if(status.error === ErrorCodes.SUCCESS) {
				Alert.show("Blob updated", "Success", mx.controls.Alert.OK);
				refreshBlobDisplay();
			} else {
				Alert.show("Blob update failed", "Error", mx.controls.Alert.OK);
			}
		}
		
		/**
		 * Trim leading and trailing spaces from a string
		 * @method trim
		 * @return {String} Trimmed string
		 */
		public function trim(s:String):String 
		{
			return s.replace(/^\s+|\s+$/g, '');
		};
		
		public function refreshBlobDisplay():void
		{
			m_ui.displayBlob.text = "Fetching...";
			var whoseBlob:String = m_ui.whoseBlobSel.selectedItem;
			var blobType:String = m_ui.blobTypeSel.selectedItem;
			if(whoseBlob == "My Blob") {
				m_storage.getUserBlobAction(blobType, updateBlobField);
			} else {
				var zid:String = m_ui.inpZid.text;
				m_storage.getFriendBlobAction(zid, blobType, updateBlobField);
			}	
		}
		public function auto_get_part(callback:Function):void
		{
			var cb:Function = function(blobType : String,status : Object, params : Object) :void 
			{
				auto_updateBlobField(blobType, status, params);
				if(!null) 
				{
					callback();
				}
			}
			m_storage.getUserBlobAction(auto_blobType, cb);
			
		}
		
		public function auto_set_part(callback:Function):void
		{
			var m_Jobject:Object = {"name":"rahul","coin":789,"level":909};
			var m_Jstring:String = JSON.stringify(m_Jobject);
			var blob:String = trim(m_Jstring);
			
			m_storage.saveUserBlobAction(auto_blobType,auto_new_cas,blob,function (status:Object,params:Object):void
			{
				auto_updateBlobStatus(status,params);
				callback();
			});
		}
		
		public function auto_fget_part(callback:Function):void
		{
			var cb:Function = function(blobType : String,status : Object, params : Object) :void 
			{
				auto_updateFriendBlobField(blobType, status, params);
				if(!null) 
				{
					callback();
				}
			}
			m_storage.getFriendBlobAction(auto_zid,auto_blobType, cb);
		}
		
		private function BlobSelhand(e:Event):void
		{
			if(m_ui.whoseBlobSel.selectedItem == "My Blob") {
				m_ui.inpZid.enabled = false;
				m_ui.setBlobBtn.enabled = true;
			} else {
				m_ui.inpZid.enabled = true;
				m_ui.setBlobBtn.enabled = false;
			}
		}
		private function getBlobBtnhand(e:MouseEvent):void
		{
			refreshBlobDisplay();
		}
		
		private function onlineOrOfflinehand(e:MouseEvent):void
		{
			m_storage.offline = !spark.components.CheckBox(e.target).selected;
		}
		private function setBlobBtnhand(e:MouseEvent):void
		{
			var blobType:String = m_ui.blobTypeSel.selectedItem;
			var blob:String = trim(m_ui.displayBlob.text);
			var cas:String = m_ui.displayCAS.text;
			m_storage.saveUserBlobAction(blobType, cas, blob, updateBlobStatus);
		}
		public function initHandlers():void
		{
			m_ui.whoseBlobSel.addEventListener(Event.CLOSE, BlobSelhand);
			
			m_ui.getBlobBtn.addEventListener(MouseEvent.CLICK, getBlobBtnhand);
			
			m_ui.onlineOrOffline.addEventListener(MouseEvent.CLICK, onlineOrOfflinehand);
			
			m_ui.setBlobBtn.addEventListener(MouseEvent.CLICK, setBlobBtnhand);
		}
		public function auto_initHandlers(callback:Function):void
		{	
			var cb_set:Function = function():void 
			{
				auto_set_part(callback);
			}
			
			var cb_complete:Function = function():void 
			{
				var cb:Function = function():void 
				{
					
					auto_fget_part(callback);
				}
				auto_set_part(cb);
			}
			
			auto_get_part(cb_complete);				// Call for complete execution of get,set,friend_get	
			//auto_fget_part(callback);				BASIC FRIEND GET FUNCTION
			//auto_get_part(cb_set);					BASIC SET FUNCTION
			//auto_get_part(callback);				BASIC GET FUNCTION
		}
	}
}
