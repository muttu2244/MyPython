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
	import flash.utils.Dictionary;
	import flash.utils.describeType;
	
	import mx.controls.Alert;
	import mx.utils.ObjectUtil;
	
	import spark.components.Button;
	
	import zynga.greyhound.client.base.Constants;
	import zynga.greyhound.client.base.ErrorCodes;
	import zynga.greyhound.client.base.IGame;
	import zynga.greyhound.client.base.IGreyhound;
	import zynga.greyhound.client.base.IMeta;
	import zynga.greyhound.client.base.ITime;
	
	public class UserMetaUIMgr
	{
		private var m_ui:Object;
		private var m_greyhound:IGreyhound;
		private var m_fields:Object;
		
		public function UserMetaUIMgr(greyhound:IGreyhound, uiControls:Object)
		{
			m_greyhound = greyhound;
			m_ui = uiControls;
			initHandlers();
		}
		public function removeHandlers():void
		{
			m_ui.getMetaBtn.removeEventListener(MouseEvent.CLICK, getMetaBtnhand);
			
			m_ui.setMetaBtn.removeEventListener(MouseEvent.CLICK, metaUserUpdateRequest);
			
			m_greyhound = null;
			m_ui = null;
		}
		public function userGetMeta_cb(status : Object, params : Object) : void
		{
			if(status.error == ErrorCodes.SUCCESS) {
				this.m_fields = params.data;
				m_ui.displayMeta.text = JSON.stringify(params.data);
			} else {
				m_ui.displayMeta.text = "Failed to get data: status=" + JSON.stringify(status) + " params=" + JSON.stringify(params);
			}
		}
		
		public function userUpdateMeta_cb(status : Object, params : Object):void
		{
			trace("userUpdateMeta_cb: status=[" + ObjectUtil.toString(status) + "] params=[", ObjectUtil.toString(params) + "]");
			if(status.error == ErrorCodes.SUCCESS) {
				m_ui.displayMeta.text = JSON.stringify(this.m_fields);
			} else {
				m_ui.displayMeta.text = "Failed to update meta: status=" + JSON.stringify(status) + " params=" + JSON.stringify(params);
				//Alert.show("Failed to update meta: status=" + JSON.encode(status) + " params=" + JSON.encode(params), "Error", mx.controls.Alert.OK);
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
		
		public function refreshMetaDisplay():void
		{
			m_ui.displayMeta.text = "Fetching...";
			m_greyhound.meta.userGetMeta(userGetMeta_cb);
		}
		
		public function metaUserUpdateRequest(e:MouseEvent):void {
			this.m_fields = JSON.parse(trim(m_ui.displayMeta.text))
			var metaFieldsDict:Dictionary = new Dictionary();
			for (var k:String in this.m_fields) {
				metaFieldsDict[ k ] = this.m_fields[ k ];
			}
			m_greyhound.meta.userUpdateMeta(metaFieldsDict, userUpdateMeta_cb);
		}
		
		private function getMetaBtnhand(e:MouseEvent):void
		{
			trace("meta.user.get:");
			refreshMetaDisplay();
		}
		
		public function initHandlers():void
		{
			m_ui.getMetaBtn.addEventListener(MouseEvent.CLICK, getMetaBtnhand);
			
			m_ui.setMetaBtn.addEventListener(MouseEvent.CLICK, metaUserUpdateRequest);
		}
	}
}