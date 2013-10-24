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
	import flash.text.TextField;
	import flash.utils.ByteArray;
	import flash.utils.describeType;
	
	import mx.collections.ArrayCollection;
	import mx.collections.ArrayList;
	import mx.controls.Alert;
	import mx.controls.CheckBox;
	import mx.utils.ObjectUtil;
	
	import spark.components.Button;
	import spark.components.HGroup;
	import spark.components.Label;
	import spark.components.VGroup;
	
	import zynga.greyhound.client.base.Constants;
	import zynga.greyhound.client.base.ErrorCodes;
	import zynga.greyhound.client.base.IGame;
	import zynga.greyhound.client.base.IGreyhound;
	import zynga.greyhound.client.base.IStorage;
	import zynga.greyhound.client.base.ITime;
	
	public class UserDeltaUIMgr
	{
		private var m_ui:Object;
		private var m_storage:Storage;
		private var m_greyhound:IGreyhound;
		
		private var auto_deltaType:String = "gift";
		private var auto_delobj:Object = {"delta_id":"rahul_updation","gift":"A lot of","level":200};
		private var auto_delstr:String = JSON.stringify(auto_delobj);
		public var auto_arr_del:ArrayCollection = new ArrayCollection();
		private var auto_obj:Object;
		private var auto_id:String;
		
		public function UserDeltaUIMgr(greyhound:IGreyhound, uiControls:Object = null)
		{
			m_greyhound = greyhound;
			m_ui = uiControls;
			m_storage = new Storage(m_greyhound);
			if (m_ui != null)
				initHandlers();
		}
		public function removeHandlers():void
		{
			m_ui.getDeltaBtn.removeEventListener(MouseEvent.CLICK,getDeltaBtnhand );
			
			m_ui.delDeltaBtn.removeEventListener(MouseEvent.CLICK,delDeltaBtnhand );
			
			m_ui.addDeltaBtn.removeEventListener(MouseEvent.CLICK,addDeltaBtnhand );
			m_greyhound = null;
			m_ui = null;
			m_storage = null;
		}
		public function updateDeltaField(status : Object, params : Object) : void
		{
			if(status.error === ErrorCodes.SUCCESS) {
				var deltas:Array = params.deltas;
				trace(deltas);
				var deltasData:Array = [];
				for(var i:int = 0; i < deltas.length; i++) {
					var deltaId:String = deltas[i].id;
					var expiryVal:String = (deltas[i].expires).toString();
					var deltaVal:String = JSON.stringify(deltas[i].value.readUTFBytes(deltas[i].value.length));
					var selectBtn:CheckBox = new CheckBox();
					selectBtn.label = "Delete";
					selectBtn.id = deltaId;
					
					deltasData.push({
						id:deltaId,
						value:deltaVal,
						expiry: expiryVal,
						selectBtn:selectBtn
					});
				}
				m_ui.updateDeltasData(deltasData);
				//m_ui.displayDelta.text = JSON.encode(deltas);
			} else {
				//m_ui.displayDelta.text = "Failed to get data";
			}
		}
		
		public function auto_updateDeltaField(status : Object, params : Object) : void
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
			auto_obj["API"] = "user.query.delta";
			auto_obj["Error Code"] = status.error;
			auto_arr_del.addItem(auto_obj);
		}
		
		public function addDeltaStatus(status : Object, params : Object):void
		{
			if(status.error === ErrorCodes.SUCCESS) {
				Alert.show("Delta added", "Success", mx.controls.Alert.OK);
				refreshDeltaList();
			} else {
				Alert.show("Delta add failed", "Error", mx.controls.Alert.OK);
			}
		}
		
		public function auto_addDeltaStatus(status : Object, params : Object):void
		{
			auto_obj = new Object();
			if(status.error === ErrorCodes.SUCCESS) 
			{		
				auto_obj["Result"] = "PASS";
				//Alert.show(ObjectUtil.toString(status));
			} 
			else 
			{
				auto_obj["Result"] = "FAIL";
			}
			auto_obj["API"] = "friend.add.delta";
			auto_obj["Error Code"] = status.error;
			auto_arr_del.addItem(auto_obj);
		}
		
		public function delDeltaStatus(status : Object):void
		{
			if(status.error === ErrorCodes.SUCCESS) {
				Alert.show("Deltas deleted", "Success", mx.controls.Alert.OK);
				refreshDeltaList();
			} else {
				Alert.show("Deltas delete failed", "Error", mx.controls.Alert.OK);
			}
		}
		
		public function auto_delDeltaStatus(status : Object):void
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
			auto_obj["API"] = "user.delete.delta";
			auto_obj["Error Code"] = status.error;
			auto_arr_del.addItem(auto_obj);
		}
		public function refreshDeltaList():void
		{
			var deltaType:String = m_ui.deltaTypeSel.selectedItem;
			m_storage.getUserDeltaAction(deltaType, updateDeltaField);
		}
		
		private function getDeltaBtnhand(e:MouseEvent):void
		{
			refreshDeltaList();
		}
		private function delDeltaBtnhand(e:MouseEvent):void
		{
			var selArr:Array = m_ui.deltasDataGrid.selectedIndices; 
			var deltaArr:Array = [];
			for(var i:int = 0; i < selArr.length; i++) {
				deltaArr.push(m_ui.deltasDataGrid.dataProvider[selArr[i]].id);
			}
			m_storage.deleteUserDeltaAction(deltaArr, delDeltaStatus);
		}
		private function addDeltaBtnhand(e:MouseEvent):void
		{
			if(m_ui.inpDelta.text == "") {
				Alert.show("Delta cannot be empty", "Error", mx.controls.Alert.OK);
			} else {
				var deltaType:String = m_ui.deltaTypeAddSel.selectedItem;
				m_storage.addUserDeltaAction(m_ui.inpDelta.text, deltaType, addDeltaStatus);
			}
		}
		
		private function auto_delDelta(id:String,callback:Function):void
		{
			var cb:Function = function(status:Object):void
			{
				auto_delDeltaStatus(status);
				callback();
			}
			var deltaArr:Array = [];
			deltaArr.push(auto_deltaType);
			m_storage.deleteUserDeltaAction(deltaArr, cb);
		}
		public function auto_getDelta(callback:Function):void
		{
			var cb:Function = function(status : Object, params : Object) : void
			{
				auto_updateDeltaField(status,params);
				if (params != null && params.deltas != null)
				{
					auto_id = params.deltas[0].id;
					auto_delDelta(auto_id,callback);
				}
				else
				{
					callback();
				}				
			}
			m_storage.getUserDeltaAction(auto_deltaType, cb);
		}
		private function auto_addDelta(callback:Function):void
		{
			var cb:Function = function(status : Object, params : Object):void
			{
				auto_addDeltaStatus(status, params);
				auto_getDelta(callback);
			}
			m_storage.addUserDeltaAction(auto_delstr, auto_deltaType, cb);
		}
		
		public function auto_initHandlers(callback:Function):void
		{/*
			var cb:Function = function(callback:Function):void
			{
			getDelta(callback);
			}
			*/	auto_addDelta(callback);
		}
		public function initHandlers():void
		{
			m_ui.getDeltaBtn.addEventListener(MouseEvent.CLICK,getDeltaBtnhand );
			
			m_ui.delDeltaBtn.addEventListener(MouseEvent.CLICK,delDeltaBtnhand );
			
			m_ui.addDeltaBtn.addEventListener(MouseEvent.CLICK,addDeltaBtnhand );
		}
	}
}
