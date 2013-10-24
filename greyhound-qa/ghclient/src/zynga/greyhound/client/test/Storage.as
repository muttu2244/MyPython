package zynga.greyhound.client.test
{
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.external.ExternalInterface;
	import flash.utils.ByteArray;
	import flash.utils.describeType;
	
	import mx.utils.ObjectUtil;
	
	import zynga.greyhound.client.base.Constants;
	import zynga.greyhound.client.base.ErrorCodes;
	import zynga.greyhound.client.base.IGame;
	import zynga.greyhound.client.base.IGreyhound;
	import zynga.greyhound.client.base.IStorage;
	import zynga.greyhound.client.base.ITime;
	
	public class Storage
	{
		private var m_greyhound:IGreyhound;
		
		public function Storage(greyhound:IGreyhound)
		{
			m_greyhound = greyhound;
		}
		
		public function getUserBlobAction(blobType:String, cbHandler:Function):void
		{
			var blobTypeArr:Array = [blobType];
			m_greyhound.storage.getUserBlobs(blobTypeArr, function(status:Object, params:Object):void {
				//Update Text through handler
				cbHandler(blobType, status, params);
			});
		}
		
		public function getFriendBlobAction(zid:String, blobType:String, cbHandler:Function):void
		{
			var blobTypeArr:Array = [blobType];
			m_greyhound.storage.getFriendBlob(zid, blobTypeArr, function(status:Object, params:Object):void {
				//Update Text through handler
				cbHandler(blobType, status, params);
			});
		}
		
		public function saveUserBlobAction(blobType:String, cas:String, blob:String, cbHandler:Function):void
		{
			var blobBytes:ByteArray = new ByteArray();
			blobBytes.writeUTFBytes(ObjectUtil.toString(JSON.parse(blob)));
			blobBytes.position = 0;
			m_greyhound.storage.saveUserBlob(blobType, blobBytes, cas, function(status:Object, params:Object):void {
				//Update saved status through handler
				cbHandler(status, params);
			});
		}
		
		public function getUserDeltaAction(deltaType:String, cbHandler:Function):void
		{
			m_greyhound.storage.getUserDeltas(function(status:Object, params:Object):void {
				cbHandler(status, params);
			}, deltaType);
		}
		
		public function addUserDeltaAction(deltaVal:String, deltaType:String, cbHandler:Function):void
		{
			var zid:String = ExternalInterface.call("Z.auth.getAuthZID");
			var byteArr:ByteArray = new ByteArray();
			byteArr.writeUTFBytes(deltaVal);
			byteArr.position = 0;
			m_greyhound.storage.addFriendDelta(zid, byteArr, deltaType, function(status:Object, params:Object):void {
				cbHandler(status, params);
			});
			
		}
		
		public function deleteUserDeltaAction(deltaArr:Array, cbHandler:Function):void
		{
			m_greyhound.storage.deleteUserDeltas(deltaArr, function(status:Object):void {
				cbHandler(status);
			});
		}
		
		public function set offline(value:Boolean):void	{
			trace("Setting offline to : " + value);
			m_greyhound.offline = value;
		}
	}
}