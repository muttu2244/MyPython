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
	import flash.system.SecurityDomain;
	import flash.utils.ByteArray;
	import flash.utils.describeType;
	
	
	import mx.containers.TabNavigator;
	
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
	
	public class Bootstrap
	{
		private var m_stage:Stage = null;
		private var m_loaderInfo:LoaderInfo = null;
		private var m_loader:Loader =  new Loader();
		private var m_context:LoaderContext = null;
		
		private var m_flashvars:Object = null;
		private var m_greyhound:IGreyhound = null;
		
		private var m_greyhoundUrl:String = "";
		
		private var m_ui:Object; //ui controls
		private var m_userBlobMgr:UserBlobUIMgr;
		private var m_userDeltaMgr:UserDeltaUIMgr;
		private var m_userMetaMgr:UserMetaUIMgr;
		private var m_userGraphMgr:UserGraphUIMgr;
		private var m_userQueryMgr:UserQueryUIMgr;
		
		public var auto_boot_arr:ArrayCollection = new ArrayCollection();
		
		public function Bootstrap(loaderInfo:LoaderInfo, stage:Stage, uiControls:Object = null)
		{
			m_loaderInfo = loaderInfo;
			m_stage = stage;
			m_ui = uiControls;
		}
		private function auto_merge_array(a:ArrayCollection,b:ArrayCollection):ArrayCollection
		{
			for each(var item:Object in b)
			{
				a.addItem(item);
			}
			return (a);
		}
		
		public function auto_initialize(callback:Function) : void
		{
			//m_greyhoundUrl = "C:\\Users\\ryadav\\Adobe Flash Builder 4.6\\greyhound-as3-win\\Greyhound\\bin-debug\\Greyhound.swf";
			
			var flashvars:Object = LoaderInfo(m_loaderInfo).parameters;
			for (var fvar:String in flashvars)
			{
				switch (fvar) {
					case "crossdomain_xml":
					{
						trace("Got a crossdomain xml");
						Security.loadPolicyFile(flashvars["crossdomain_xml"]);
					}
						break;
					case "greyhound_url":
					{
						m_greyhoundUrl = flashvars["greyhound_url"];
					}
						break;
					default :
					{
					}
						break; // not the for, but the switch
				}
			}
			
			this.m_flashvars = flashvars;
			
			
			m_context = new LoaderContext();
			
			m_context.securityDomain = SecurityDomain.currentDomain;
			m_context.checkPolicyFile = true;
			
			m_loader.contentLoaderInfo.addEventListener(Event.COMPLETE, auto_initializeGreyhound);
			m_loader.load(new URLRequest(m_greyhoundUrl), m_context);
			
			function auto_initializeGreyhound(ev: Event) : void
			{
				
				m_greyhound = (ev.currentTarget.content as IGreyhound);
				auto_init(m_flashvars, m_stage, m_greyhound,callback);
			}
		}
		public function initialize() : void
		{
			//m_greyhoundUrl = "C:\\Users\\ryadav\\Adobe Flash Builder 4.6\\greyhound-as3-win\\Greyhound\\bin-debug\\Greyhound.swf";
			
			var flashvars:Object = LoaderInfo(m_loaderInfo).parameters;
			
			for (var fvar:String in flashvars)
			{
				switch (fvar) {
					case "crossdomain_xml":
					{
						trace("Got a crossdomain xml");
						Security.loadPolicyFile(flashvars["crossdomain_xml"]);
					}
						break;
					case "greyhound_url":
					{
						m_greyhoundUrl = flashvars["greyhound_url"];
					}
						break;
					default :
					{
					}
						break; // not the for, but the switch
				}
			}
			
			this.m_flashvars = flashvars;
			
			m_context = new LoaderContext();
			
			m_loader.contentLoaderInfo.addEventListener(Event.COMPLETE, initializeGreyhound);
			m_loader.load(new URLRequest(m_greyhoundUrl), m_context);
		}
		
		
		public function initializeGreyhound(ev: Event) : void
		{
			m_greyhound = (ev.currentTarget.content as IGreyhound);
			this.init(m_flashvars, m_stage, m_greyhound);	
		}
		
		public function init(params : Object, stageReference : Stage, greyhound : IGreyhound, local:Boolean=false):Boolean
		{
			m_greyhound = greyhound;
			if(m_greyhound.init(Constants.ABI_VERSION, params))
			{
				//throw exception
				//return false;
			}
			
			m_userBlobMgr = new UserBlobUIMgr(m_greyhound, m_ui.userBlob);
			m_userDeltaMgr = new UserDeltaUIMgr(m_greyhound, m_ui.userDelta);
			m_userMetaMgr = new UserMetaUIMgr(m_greyhound, m_ui.userMeta);
			m_userGraphMgr = new UserGraphUIMgr(m_greyhound, m_ui.userGraph);
			m_userQueryMgr = new UserQueryUIMgr(m_greyhound, m_ui.userQuery);
			
			return true;
		}
		
		public function auto_init(params : Object, stageReference : Stage, greyhound : IGreyhound, callback:Function ,local:Boolean=false):Boolean
		{
			m_greyhound = greyhound;
			
			if(m_greyhound.init(Constants.ABI_VERSION, params))
			{
				//throw exception
				//return false;
			}	
			m_userBlobMgr = new UserBlobUIMgr(m_greyhound);
			m_userDeltaMgr = new UserDeltaUIMgr(m_greyhound);
			
			// NOW I AM NESTING THE INIT HANDLER OF DELTA INTO BLOB SO AS TO MAINTAIN  SEQUENTIALITY
			m_userBlobMgr.auto_initHandlers(function ():void {
				
				auto_boot_arr = auto_merge_array(auto_boot_arr,m_userBlobMgr.auto_arr_blb);
				
				m_userDeltaMgr.auto_initHandlers(function():void {
					
					auto_boot_arr = auto_merge_array(auto_boot_arr,m_userDeltaMgr.auto_arr_del);
					callback();
				});
			});
				
			return true;
		}
		
		public function teardown():void
		{
			m_userBlobMgr.removeHandlers();
			m_userDeltaMgr.removeHandlers();
			m_userMetaMgr.removeHandlers();
			m_userGraphMgr.removeHandlers();
			m_userQueryMgr.removeHandlers();
						
			m_stage = null;
			m_loaderInfo = null;
			m_loader =  null;
			m_context = null;
			
			m_flashvars = null;
			m_greyhound = null;
			
			m_greyhoundUrl = null;
			
			m_ui = null; //ui controls
			m_userBlobMgr = null;
			m_userDeltaMgr = null;
			m_userMetaMgr = null;
			m_userGraphMgr = null;
			m_userQueryMgr = null;
			
		}
	}
}
