# 基本语法
1. 过程和业务变量
```sql
CREAT OR REPLACE PROCEDURE procedure_name(I_param in CHAR,
                                          O_param out VARCHAR2,
                                          O_param0  out VARCHAR2) IS 

-------------------------------调试变量------------------------------
v_msg varchar2(200); --返回信息
v_error integer;
v_object varchar2(50) default 'procedure_name'; --标记操作对象

-------------------------------业务变量-------------------------------
--用于处理业务的临时变量
v_date char(8); --业务时间
v_name1 number(19,4); --业务变量1
v_name2 varchar(20) ; --业务变量2
```
2. 业务处理
```sql
BEGIN
--------------------------------业务处理-------------------------------

-----------变量赋值--
O_param0 := 0
O_param := '开始执行'; --  :=用于赋值，=用于判断
v_date:=I_param; --in类型的变量

-----------创建临时表（有时会用到）--
execute immediate 'truncate table table_name';

-----------可能用到的结构--
for idx in (select t.* from table1 t) loop
  v_name1 := idx.name1;
  v_name2 := idx.name2;
  if to_date(v_date,'yyyymmdd')+1>=num then
    v_date := to_char(to_date(v_date,'yyyymmdd')+5,'yyyymmdd');
  end if;
  insert into table_name(var1,var2)
    select var1,var2 from t1
    where not exists(select * from table_name d
                     where d.var1=v_date); --exists用于挑选table_name中的数据
  commit; --注意要commit，否则数据库中不会变
end loop;

-----------主表table_mian--
insert into table_mian
  (var1,
  case
    when t.var like '%-12-01%' then -- %通配符
      '2019-12-3'
    else
      coalesce(t.var,'2019-11-01') -- coalesce按顺序选择非null值
    end var2，-- end后面还可以继续case
    '@'
select t.* from table_name t
  left join table1 a
  where t.id=a.id;
commit;
```
3. 错误处理
```sql
-------------------------------业务结束------------------------------
O_param0 := 0 -- 即正常运行为0
O_param :='执行成功'
EXCEPTION
  when OTHERS then
    O_param0 := SQLCODE; -- 错误码
    O_param := O_param || SQLERRM; --SQLERRM错误代码错误信息
    ROLLBACK; --回调，回调没有commit或者commit出错的部分
    v_error := O_param0;
    v_msg := O_param;
    -- 一般还会将错误信息写入log
END;
```
4. oracle视图，主要用于表的查询，可结合存储过程使用
```sql
--------------------------------基本语法-----------------------------
create or replace view view_name as 
select t.var1,
       t.var2
from t_name t
left join t1_name a
  where t.id=a.id;
```
