DELETE_ATTR = """delete from pmd.product_value where value_spec_id in (select id from pmd.value where attribute_id in (select id from pmd.attribute where name ilike '%test%'));
delete from  pmd.outbox_attribute where entity_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.specification_attribute where attribute_id in (select id from pmd.attribute where name ilike '%test%');
delete from pmd.value_story where value_id in (select id from pmd.value where attribute_id in (select id from pmd.attribute where name ilike '%test%'));
delete from  pmd.value where attribute_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.attribute_story where attribute_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.product_attribute where attribute_spec_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.specification_attribute_story where attribute_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.attribute_role where attribute_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.attribute_role_story where attribute_id in (select id from pmd.attribute where name ilike '%test%');
delete from  pmd.product_story_attribute where attribute_spec_id in (select id from pmd.attribute where name ilike '%test%');
delete from pmd.attribute where name ilike '%test%'"""

DELETE_SPEC = """delete from  pmd.specification_story where specification_id in (select id from pmd.specification where name ilike '%test%');
delete from pmd.outbox_specification where outbox_specification.entity_id in (select id from pmd.specification where name ilike '%test%');
delete from  pmd.specification_attribute_story where specification_id in (select id from pmd.specification where name ilike '%test%');
delete from pmd.specification where name ilike '%test%'"""

DELETE_ROLE = """delete from pmd.role_story where role_id in (select id from pmd.role where name ilike '%test%');
delete from pmd.user_role where role_id in (select id from pmd.role where name ilike '%test%');
delete from pmd.user_role_story where role_id in (select id from pmd.role where name ilike '%test%');
delete from pmd.attribute_role_story where role_id in (select id from pmd.role where name ilike '%test%');
delete from pmd.attribute_role where role_id in (select id from pmd.role where name ilike '%test%');
delete from pmd.role where name ilike '%test%'"""

DELETE_SOURCE = """delete from  pmd.outbox_attribute where entity_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from  pmd.specification_attribute where attribute_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from  pmd.attribute_story where attribute_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from  pmd.product_attribute where attribute_spec_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from  pmd.specification_attribute_story where attribute_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from  pmd.attribute_role where attribute_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from  pmd.attribute_role_story where attribute_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from pmd.product_story_attribute where attribute_spec_id in (select id from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%'));
delete from pmd.attribute where source_id in (select id from pmd.source where name ilike '%test%');
delete from pmd.source where name ilike '%test%'"""

DELETE_DOCS = """delete FROM pmd.file WHERE product_file_id in (SELECT id FROM pmd.product_file WHERE name ILIKE '%test%' or name ILIKE '%Паспорт критичности 2025%');
delete FROM pmd.product_file_story WHERE product_file_id in (SELECT id FROM pmd.product_file WHERE name ILIKE '%test%' or name ILIKE '%Паспорт критичности 2025%');
delete FROM pmd.product_file WHERE name ILIKE '%test%' or name ILIKE '%Паспорт критичности 2025%'"""

DELETE_CRITICALITY_CLASS_MESSAGE = """delete from pmd.integration_message
where topic like 'criticality_class_inbox'"""

DELETE_PRODUCTS = """CREATE TEMPORARY TABLE temp_product_ids AS
SELECT id FROM pmd.product WHERE name ILIKE '%test%';

DELETE FROM pmd.product_attribute WHERE product_attribute.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.outbox_product WHERE outbox_product.entity_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.product_story_old WHERE product_story_old.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.product_story_v2 WHERE product_story_v2.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.product_capability WHERE product_capability.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.product_service WHERE product_service.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.section WHERE section.product_id IN (SELECT id FROM temp_product_ids);

CREATE TEMPORARY TABLE temp_product_file_ids AS
SELECT id FROM pmd.product_file WHERE product_id IN (SELECT id FROM temp_product_ids);

DELETE FROM pmd.product_file_story WHERE product_file_id IN (SELECT id FROM temp_product_file_ids);
DELETE FROM pmd.file WHERE product_file_id IN (SELECT id FROM temp_product_file_ids);
DELETE FROM pmd.product_file WHERE product_file.product_id IN (SELECT id FROM temp_product_ids);

DELETE FROM pmd.product_demo WHERE product_demo.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.delegation WHERE delegation.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.product_value WHERE product_value.product_id IN (SELECT id FROM temp_product_ids);
DELETE FROM pmd.favorite_product WHERE favorite_product.product_id IN (SELECT id FROM temp_product_ids);

CREATE TEMPORARY TABLE temp_mailing_ids AS
SELECT id FROM pmd.mailing WHERE mailing.product_id IN (SELECT id FROM temp_product_ids);

DELETE FROM pmd.mailing_response WHERE mailing_response.mailing_id IN (SELECT id FROM temp_mailing_ids);
DELETE FROM pmd.mailing WHERE mailing.product_id IN (SELECT id FROM temp_product_ids);

DELETE FROM pmd.product WHERE id IN (SELECT id FROM temp_product_ids);"""

DELETE_BRIEFS = """delete from pb.brief_executor where brief_id in (select id from pb.brief where ((login IN ('regular_user','regular_user','admin_user')) AND (status IN ('statusDeclined','statusDone','statusInWork','statusPublished', 'statusApproval'))));
delete from pb.brief where id in (select id from pb.brief where ((login IN ('regular_user','regular_user','admin_user')) AND (status IN ('statusDeclined','statusDone','statusInWork','statusPublished', 'statusApproval'))))
"""

DELETE_NOTI_NOTIFICATION_BD = """delete from ntf.email_history
"""

DELETE_NOTI_PRODUCTSTORAGE_BD = """delete from pmd.message_outbox
"""

DELETE_NOTI_PRODBOARD_BD = """delete from pb.message_outbox
"""

DELETE_ACTION = """delete from pmd.action_employee where action_employee.action_id in (select id from pmd.action where name ilike '%test%');
delete from pmd.action_file where action_file.action_id in (select id from pmd.action where name ilike '%test%');
delete from pmd.action_link where action_link.action_id in (select id from pmd.action where name ilike '%test%');
delete from pmd.action where action.main_action in (select id from pmd.action where name ilike '%test%');
delete from pmd.action_action_group where action_action_group.action_id in (select id from pmd.action where name ilike '%test%');
delete from pmd.action_filter where action_filter.action_id in (select id from pmd.action where name ilike '%test%');
delete from pmd.action where name ilike '%test%' """

DELETE_TOOLS_AND_GROUPS = """
UPDATE pmd.tool_file
SET tool_id = NULL
WHERE tool_id IN (
    SELECT t.id
    FROM pmd.tool t
    JOIN pmd.tool_group g ON t.group_id = g.id
    WHERE g.name ILIKE '%test%'
);

DELETE FROM pmd.tool_group WHERE name ILIKE '%test%';"""

GET_ATOMIC = """SELECT p.code, p.name, p.id, pv.created_at, pv.id
FROM pmd.product p
         INNER JOIN pmd.product_attribute pa ON pa.product_id = p.id
         INNER JOIN pmd.attribute a ON a.id = pa.attribute_spec_id AND a.code = 'PPInfo_main_product'
         INNER JOIN pmd.product_value pv ON pv.attribute_id = pa.id
where pv.product_id IS NOT NULL;
"""

DELETE_BRIEFS_V2 = """delete from  pb.brief_executor where brief_id in (select id FROM pb.brief WHERE data::text LIKE '%test%');
DELETE FROM pb.brief WHERE data::text LIKE '%test%';"""

DELETE_DEMOS = """delete from pmd.product_demo where demo_id in (select id from pmd.demo where name ilike '%test%');
delete from pmd.demo where name ilike '%test%';
"""

DELETE_DEMOS_CATEGORIES = """delete from pmd.demo_categories where name ilike '%test%';
"""

DELETE_INTEGRATION_MESSAGE = """DELETE FROM pmd.integration_message
"""
