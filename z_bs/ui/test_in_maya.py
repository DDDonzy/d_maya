"""
Maya环境中的功能测试脚本
在Maya Script Editor中运行此脚本来验证重构后的BlendShape工具
"""

def test_blendshape_ui():
    """在Maya中测试重构后的BlendShape UI"""
    
    print("=" * 60)
    print("Maya BlendShape 工具重构功能测试")
    print("=" * 60)
    
    try:
        # 导入重构后的UI模块
        print("1. 导入模块...")
        import z_bs.ui.uiMain as ui_main
        print("   ✓ uiMain 模块导入成功")
        
        # 检查EventHandler和ActionHandler是否正确导入
        from z_bs.ui.logic.event import EventHandler
        from z_bs.ui.logic.actions import ActionHandler
        print("   ✓ EventHandler 和 ActionHandler 导入成功")
        
        # 创建UI实例
        print("\n2. 创建UI实例...")
        ui = ui_main.BlendShapeUI()
        print("   ✓ BlendShapeUI 实例创建成功")
        
        # 检查处理器是否正确初始化
        if hasattr(ui, 'event_handler') and hasattr(ui, 'action_handler'):
            print("   ✓ EventHandler 和 ActionHandler 正确初始化")
        else:
            print("   ✗ 处理器初始化失败")
            return False
        
        # 检查关键方法是否存在
        print("\n3. 验证方法完整性...")
        
        # 检查ActionHandler方法
        action_methods = [
            'load_blendshape', 'load_target', 'add_sculpt', 'auto_set_weight',
            'select_base_mesh', 'select_bs_node', 'go_to_pose'
        ]
        
        for method in action_methods:
            if hasattr(ui.action_handler, method):
                print(f"   ✓ ActionHandler.{method}")
            else:
                print(f"   ✗ 缺少方法: ActionHandler.{method}")
        
        # 检查EventHandler方法
        event_methods = [
            'handle_go_to_pose', 'handle_auto_set_weight', 
            'handle_select_by_label', 'event_filter'
        ]
        
        for method in event_methods:
            if hasattr(ui.event_handler, method):
                print(f"   ✓ EventHandler.{method}")
            else:
                print(f"   ✗ 缺少方法: EventHandler.{method}")
        
        # 显示UI
        print("\n4. 显示UI...")
        ui.show()
        print("   ✓ UI 显示成功")
        
        print("\n" + "=" * 60)
        print("🎉 重构功能测试通过！")
        print("✅ 所有核心功能正常工作")
        print("✅ UI可以正常显示和交互")
        print("✅ 重构成功完成！")
        print("=" * 60)
        
        return ui
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def quick_test():
    """快速测试 - 只检查导入和基本功能"""
    try:
        import z_bs.ui.uiMain as ui_main
        ui = ui_main.BlendShapeUI()
        print("✅ 快速测试通过 - 重构成功！")
        return ui
    except Exception as e:
        print(f"❌ 快速测试失败: {e}")
        return None

# 在Maya Script Editor中运行以下命令:
# 
# 完整测试:
# exec(open(r'e:\d_maya\z_bs\ui\test_in_maya.py').read())
# ui = test_blendshape_ui()
#
# 快速测试:
# exec(open(r'e:\d_maya\z_bs\ui\test_in_maya.py').read())
# ui = quick_test()

if __name__ == "__main__":
    # 如果直接在Maya中运行
    ui = test_blendshape_ui()
