import os
import pickle
import random
import uuid

import pygame

from base import ConstructionCrane, Laboratory
from map import Base, ResourceSite, MapEvent


def everyday_interaction(r_queue, base_inst, dc, map_events, surface_img_dict):
    if dc == 0:
        com = None
        while com not in ['0', '1']:
            com = input('0.新游戏 1.继续游戏')
            if com == '0':
                r_queue, base_inst, surface_img_dict = first_day(r_queue, surface_img_dict)
                dc += 1
                break
            elif com == '1':
                loaded = load_game()
                if None in loaded:
                    com = None
                else:
                    base_inst, img_dict, dc = loaded
            else:
                print('指令错误！')
    else:
        print('今天是第' + str(dc + 1) + '天')
        com = input('输入指令')
        if com == 'tomorrow':
            map_events, r_queue, surface_img_dict = after_1_day(
                base_inst,
                map_events,
                r_queue,
                surface_img_dict
            )
            dc += 1
        else:
            if com == 'stats':
                display_stat(base_inst)
            elif com == 'build':
                build_module(base_inst)
            elif com == 'design':
                design_module(base_inst)
            elif com == 'tasks':
                tasks_module(base_inst)
            elif com == 'factory':
                factory_module(base_inst)
            elif com == 'save':
                save_game(base_inst, surface_img_dict, dc)
            elif com == 'load':
                load_game()
            else:
                print('指令错误')
    return r_queue, base_inst, dc, map_events, surface_img_dict


def display_stat(base_inst: Base):
    pass


def build_module(base_inst: Base):
    crane_list = []
    for i in range(len(base_inst.buildings)):
        if type(base_inst.buildings[i]) is ConstructionCrane:
            crane_list.append(base_inst.buildings[i])
    if len(crane_list) <= 0:
        print('基地里没有塔吊！')
    else:
        print(crane_list)
        crane_no = input('输入塔吊编号')
        if crane_no.isdigit() and 0 <= int(crane_no) < len(crane_list):
            selected_crane: ConstructionCrane = crane_list[int(crane_no)]
            flag = True
            while flag:
                building_com = input('0.显示所有建筑 1.建造新建筑 2.拆除旧建筑 3.返回')
                if building_com == '0':
                    print(base_inst.buildings)
                elif building_com == '1':
                    slot_index = base_inst.next_building_slot()
                    building_type = input('请输入建筑类型代号')
                    selected_crane.build_new(slot_index, building_type)
                elif building_com == '2':
                    slot_index = input('请输入建筑槽位编号')
                    if slot_index.isdigit():
                        selected_crane.remove_old(int(slot_index))
                    else:
                        print('输入有误！')
                        continue
                elif building_com == '3':
                    break
                else:
                    print('输入有误！')
                    continue
                building_com = '-1'
                while building_com not in ['0', '1']:
                    building_com = input('0.继续 1.返回')
                    if building_com == '0':
                        flag = True
                        break
                    elif building_com == '1':
                        flag = False
                        break
                    else:
                        print('输入有误！')
        else:
            print('输入有误！')


def design_module(base_inst: Base):
    lab_list = []
    for i in range(len(base_inst.buildings)):
        if type(base_inst.buildings[i]) is Laboratory:
            lab_list.append(base_inst.buildings[i])
    if len(lab_list) <= 0:
        print('基地里没有实验室！')
    else:
        print(lab_list)
        lab_no = input('输入实验室编号')
        if lab_no.isdigit() and 0 <= int(lab_no) < len(lab_list):
            selected_lab: Laboratory = lab_list[int(lab_no)]
            flag = True
            while flag:
                print('0.显示所有零件 1.显示所有设计 2.研究新零件 3.销毁旧零件')
                research_com = input('4.中止研究 5.创建新设计 6.销毁旧设计 7.返回')
                if research_com == '0':
                    print(base_inst.unlocked_parts)
                elif research_com == '1':
                    print(base_inst.loaded_designs)
                elif research_com == '2':
                    part_type = input('请输入零件类型代号')
                    if part_type in selected_lab.part_class_dict:
                        selected_lab.research_new_part(part_type)
                    else:
                        print('输入有误！')
                        continue
                elif research_com == '3':
                    part_type = input('请输入零件类型代号')
                    if part_type in selected_lab.part_class_dict:
                        print('该类零件如下：')
                        for p in base_inst.unlocked_parts[part_type]:
                            attrs = [item for item in dir(p) if not item.startswith('__')]
                            for attr in attrs:
                                attr_val = getattr(p, attr)
                                if not hasattr(attr_val, '__call__'):
                                    print(attr, attr_val)
                        slot_index = input('请输入待删零件编号')
                        if slot_index.isdigit():
                            selected_lab.dispose_old_part(part_type=part_type, part_index=int(slot_index))
                        else:
                            print('输入有误！')
                            continue
                    else:
                        print('输入有误！')
                        continue
                elif research_com == '4':
                    print('正在进行的研究如下：')
                    for work in selected_lab.current_work:
                        print(work)
                    slot_index = input('请输入待中止研究编号')
                    if slot_index.isdigit():
                        selected_lab.terminate_ongoing_res(work_index=int(slot_index))
                    else:
                        print('输入有误！')
                        continue
                elif research_com == '5':
                    selected_lab.compose_new_design()
                elif research_com == '6':
                    print(base_inst.loaded_designs.keys())
                    name = input('输入要删除的设计名称')
                    selected_lab.delete_old_design(design_name=name)
                elif research_com == '7':
                    break
                else:
                    print('输入有误！')
                    continue
                building_com = '-1'
                while building_com not in ['0', '1']:
                    building_com = input('0.继续 1.返回')
                    if building_com == '0':
                        flag = True
                        break
                    elif building_com == '1':
                        flag = False
                        break
                    else:
                        print('输入有误！')
        else:
            print('输入有误！')


def tasks_module(base_inst: Base):
    pass


def factory_module(base_inst: Base):
    pass


def map_events_update(map_events, r_queue):
    # todo
    x = random.randint(0, 2028)
    y = random.randint(0, 1223)
    new_event = ResourceSite(x, y, 'wood', 5000)
    icon_id = str(uuid.uuid4())
    new_event.set_icon_id(icon_id)
    map_events.append(new_event)
    r_task_1 = ['load_new', new_event.get_icon_id(), 'wood.png', new_event.get_screen_pos()]
    r_queue.append(r_task_1)
    if len(map_events) > 10:
        removed_event: MapEvent = map_events.pop(0)
        r_task_2 = ['delete_old', removed_event.icon_id, None, None]
        r_queue.append(r_task_2)
        del removed_event
    return map_events, r_queue


def after_1_day(base_inst: Base, map_events, r_queue, surface_img_dict):
    for obj in base_inst.time_passed_tasks:
        obj.tomorrow()
    map_events, r_queue = map_events_update(map_events, r_queue)
    r_queue, surface_img_dict = surfaces_render_queue(r_queue, surface_img_dict)
    return map_events, r_queue, surface_img_dict


def first_day(r_queue, surface_img_dict):
    base_inst = Base(1014, 612)
    base_inst.set_icon_id(str(uuid.uuid4()))
    r_task = ['load_new', base_inst.get_icon_id(), 'base.png', base_inst.get_screen_pos()]
    r_queue.append(r_task)
    r_queue, surface_img_dict = surfaces_render_queue(r_queue, surface_img_dict)
    print('今天是第1天')
    input('按任意键继续')
    print('送你一个塔吊，不然你啥都建不了')
    slot_index = base_inst.next_building_slot()
    base_inst.buildings[slot_index] = ConstructionCrane(slot_index, base_inst)
    input('按任意键继续')
    print('再给你一些物资')
    base_inst.add_resource('wood', 100)
    base_inst.add_resource('concrete', 101)
    input('按任意键继续')
    return r_queue, base_inst, surface_img_dict


def img_dict_2_pickle(s_img_dict):
    p_dict = {}
    for img_id in s_img_dict:
        rect = s_img_dict[img_id][1].center
        path = s_img_dict[img_id][2]
        p_list = [rect, path]
        p_dict.__setitem__(img_id, p_list)
    return p_dict


def pickle_2_img_dict(p_dict):
    s_img_dict = {}
    for img_id in p_dict:
        rect_center = p_dict[img_id][0]
        path = p_dict[img_id][1]
        surface = pygame.image.load(path)
        rect = surface.get_rect(center=rect_center)
        s_img_dict.__setitem__(img_id, [surface, rect, path])
    return s_img_dict


def save_game(base_inst: Base, surface_img_dict, dc):
    hbs = os.path.exists('base.bin')
    his = os.path.exists('img_dict.bin')
    hds = os.path.exists('day_count.bin')
    if hbs and his and hds:
        save_com = input('0.覆盖存档 1.取消保存')
        if save_com == '0':
            with open('base.bin', 'wb') as f:
                pickle.dump(base_inst, f)
            with open('img_dict.bin', 'wb') as f:
                pickle_img_dict = img_dict_2_pickle(surface_img_dict)
                pickle.dump(pickle_img_dict, f)
            with open('day_count.bin', 'wb') as f:
                pickle.dump(dc, f)
            print('存档保存完毕。')
        elif save_com == '1':
            print('存档作业已中止。')
        else:
            print('指令错误，存档作业已中止。')
    else:
        with open('base.bin', 'wb') as f:
            pickle.dump(base_inst, f)
        with open('img_dict.bin', 'wb') as f:
            pickle_img_dict = img_dict_2_pickle(surface_img_dict)
            pickle.dump(pickle_img_dict, f)
        with open('day_count.bin', 'wb') as f:
            pickle.dump(dc, f)
        print('存档保存完毕。')


def load_game():
    hbs = os.path.exists('base.bin')
    his = os.path.exists('img_dict.bin')
    hds = os.path.exists('day_count.bin')
    if hbs and his and hds:
        with open('base.bin', 'rb') as f:
            base_inst = pickle.load(f)
        with open('img_dict.bin', 'rb') as f:
            pickle_img_dict = pickle.load(f)
            surface_img_dict = pickle_2_img_dict(pickle_img_dict)
        with open('day_count.bin', 'rb') as f:
            dc = pickle.load(f)
        print('存档读取完毕。')
        return base_inst, surface_img_dict, dc
    else:
        print('没有存档文件或存档文件不完整，读档作业已中止')
        return None, None, None


def surfaces_render_queue(r_queue, surface_img_dict):
    for render_task in r_queue:
        task_type = render_task[0]
        img_id = render_task[1]
        img_path = render_task[2]
        img_pos = render_task[3]
        if task_type == 'load_new':
            new_img = pygame.image.load(img_path)
            new_rect = new_img.get_rect()
            new_rect.center = tuple(img_pos)
            surface_img_dict[img_id] = [new_img, new_rect, img_path]
        elif task_type == 'move_old':
            surface_img_dict[img_id][1] = tuple(img_pos)
        elif task_type == 'delete_old':
            del surface_img_dict[img_id]
    r_queue.clear()
    return r_queue, surface_img_dict