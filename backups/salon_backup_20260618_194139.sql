--
-- PostgreSQL database dump
--

\restrict yraog5QOpTJf270hka7dccMGMXHH0xmhR1UEdglQPpZCATJ2KbtbKUntzCcMq0x

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.salon_user_user_permissions DROP CONSTRAINT IF EXISTS salon_user_user_permissions_user_id_9b6d5e12_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_user_user_permissions DROP CONSTRAINT IF EXISTS salon_user_user_perm_permission_id_c90b485d_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.salon_user_groups DROP CONSTRAINT IF EXISTS salon_user_groups_user_id_094b69f5_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_user_groups DROP CONSTRAINT IF EXISTS salon_user_groups_group_id_fe6da36e_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.salon_user DROP CONSTRAINT IF EXISTS salon_user_branch_id_3f9bdf84_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_stockmovement DROP CONSTRAINT IF EXISTS salon_stockmovement_reference_invoice_id_68ee283c_fk_salon_inv;
ALTER TABLE IF EXISTS ONLY public.salon_stockmovement DROP CONSTRAINT IF EXISTS salon_stockmovement_reference_consumptio_819c2b57_fk_salon_con;
ALTER TABLE IF EXISTS ONLY public.salon_stockmovement DROP CONSTRAINT IF EXISTS salon_stockmovement_product_id_d750188e_fk_salon_product_id;
ALTER TABLE IF EXISTS ONLY public.salon_stockmovement DROP CONSTRAINT IF EXISTS salon_stockmovement_created_by_id_43cfe1db_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_stockmovement DROP CONSTRAINT IF EXISTS salon_stockmovement_branch_id_f4cd3c25_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_service DROP CONSTRAINT IF EXISTS salon_service_category_id_0a191ae7_fk_salon_category_id;
ALTER TABLE IF EXISTS ONLY public.salon_salonsettings DROP CONSTRAINT IF EXISTS salon_salonsettings_branch_id_9bd80141_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_salarypayment DROP CONSTRAINT IF EXISTS salon_salarypayment_employee_id_6029a968_fk_salon_employee_id;
ALTER TABLE IF EXISTS ONLY public.salon_salarypayment DROP CONSTRAINT IF EXISTS salon_salarypayment_created_by_id_30e722e8_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_salarypayment DROP CONSTRAINT IF EXISTS salon_salarypayment_branch_id_b7b115a2_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_salarypayment DROP CONSTRAINT IF EXISTS salon_salarypayment_bank_id_fc228f9f_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoice DROP CONSTRAINT IF EXISTS salon_purchaseinvoice_created_by_id_3fa0c4dc_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoice DROP CONSTRAINT IF EXISTS salon_purchaseinvoice_branch_id_5450c4b5_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoiceitem DROP CONSTRAINT IF EXISTS salon_purchaseinvoic_purchase_id_07aadb38_fk_salon_pur;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoiceitem DROP CONSTRAINT IF EXISTS salon_purchaseinvoic_product_id_13c22bd7_fk_salon_pro;
ALTER TABLE IF EXISTS ONLY public.salon_product DROP CONSTRAINT IF EXISTS salon_product_category_id_ac41de83_fk_salon_category_id;
ALTER TABLE IF EXISTS ONLY public.salon_product DROP CONSTRAINT IF EXISTS salon_product_branch_id_fdd06562_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoiceitem DROP CONSTRAINT IF EXISTS salon_invoiceitem_service_id_9066907a_fk_salon_service_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoiceitem DROP CONSTRAINT IF EXISTS salon_invoiceitem_product_id_79fd85f4_fk_salon_product_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoiceitem DROP CONSTRAINT IF EXISTS salon_invoiceitem_invoice_id_55d43681_fk_salon_invoice_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_customer_id_36323656_fk_salon_customer_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_created_by_id_96e7d717_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_branch_id_af606db1_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_booking_id_cd1bbc2e_fk_salon_booking_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_barber_id_1bd1ab65_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_bank_id_1555431b_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.salon_financialledger DROP CONSTRAINT IF EXISTS salon_financialledger_created_by_id_f10ff774_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_financialledger DROP CONSTRAINT IF EXISTS salon_financialledger_branch_id_7408aafc_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_financialledger DROP CONSTRAINT IF EXISTS salon_financialledger_bank_id_e9399aeb_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensevoucher DROP CONSTRAINT IF EXISTS salon_expensevoucher_expense_type_id_af93f514_fk_salon_exp;
ALTER TABLE IF EXISTS ONLY public.salon_expensevoucher DROP CONSTRAINT IF EXISTS salon_expensevoucher_created_by_id_3533d17c_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensevoucher DROP CONSTRAINT IF EXISTS salon_expensevoucher_branch_id_c68d0249_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensevoucher DROP CONSTRAINT IF EXISTS salon_expensevoucher_bank_id_e66b30dc_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensetype DROP CONSTRAINT IF EXISTS salon_expensetype_branch_id_48151b1c_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensereturn DROP CONSTRAINT IF EXISTS salon_expensereturn_expense_id_1d1821e9_fk_salon_expense_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensereturn DROP CONSTRAINT IF EXISTS salon_expensereturn_created_by_id_00eb4aba_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensereturn DROP CONSTRAINT IF EXISTS salon_expensereturn_branch_id_53b66006_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_expensereturn DROP CONSTRAINT IF EXISTS salon_expensereturn_bank_id_4a262084_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_salary_payment_id_a7c0e376_fk_salon_sal;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_created_by_id_551ba982_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_category_id_65c4dbfd_fk_salon_category_id;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_branch_id_098eee01_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_bank_id_8594a1c2_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.salon_employeeadvance DROP CONSTRAINT IF EXISTS salon_employeeadvance_employee_id_b152d06e_fk_salon_employee_id;
ALTER TABLE IF EXISTS ONLY public.salon_employeeadvance DROP CONSTRAINT IF EXISTS salon_employeeadvance_created_by_id_5838ec1e_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_employeeadvance DROP CONSTRAINT IF EXISTS salon_employeeadvance_branch_id_51406523_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_employeeadvance DROP CONSTRAINT IF EXISTS salon_employeeadvanc_deducted_in_id_e54a65cc_fk_salon_sal;
ALTER TABLE IF EXISTS ONLY public.salon_employee DROP CONSTRAINT IF EXISTS salon_employee_user_id_166684b7_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_employee DROP CONSTRAINT IF EXISTS salon_employee_branch_id_7437cae7_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_documentcounter DROP CONSTRAINT IF EXISTS salon_documentcounter_branch_id_1a4031d7_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_dailyqueuenumber DROP CONSTRAINT IF EXISTS salon_dailyqueuenumber_branch_id_ffb4a075_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_customer DROP CONSTRAINT IF EXISTS salon_customer_branch_id_31e29fd8_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoice DROP CONSTRAINT IF EXISTS salon_consumptioninvoice_branch_id_415a54df_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoiceitem DROP CONSTRAINT IF EXISTS salon_consumptioninv_product_id_906ffb53_fk_salon_pro;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoice DROP CONSTRAINT IF EXISTS salon_consumptioninv_created_by_id_ad81fe2a_fk_salon_use;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoiceitem DROP CONSTRAINT IF EXISTS salon_consumptioninv_consumption_id_fe35927a_fk_salon_con;
ALTER TABLE IF EXISTS ONLY public.salon_booking_services DROP CONSTRAINT IF EXISTS salon_booking_services_service_id_2a25587b_fk_salon_service_id;
ALTER TABLE IF EXISTS ONLY public.salon_booking_services DROP CONSTRAINT IF EXISTS salon_booking_services_booking_id_057e3f36_fk_salon_booking_id;
ALTER TABLE IF EXISTS ONLY public.salon_booking DROP CONSTRAINT IF EXISTS salon_booking_branch_id_160fe177_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_booking DROP CONSTRAINT IF EXISTS salon_booking_barber_id_ccf3b0b9_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_bank DROP CONSTRAINT IF EXISTS salon_bank_branch_id_bb0b927c_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_auditlog DROP CONSTRAINT IF EXISTS salon_auditlog_user_id_8164f1a3_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_auditlog DROP CONSTRAINT IF EXISTS salon_auditlog_branch_id_7f2ca72f_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_advancereturn DROP CONSTRAINT IF EXISTS salon_advancereturn_created_by_id_e3e7d4b5_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.salon_advancereturn DROP CONSTRAINT IF EXISTS salon_advancereturn_branch_id_caff267b_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.salon_advancereturn DROP CONSTRAINT IF EXISTS salon_advancereturn_advance_id_e5e34887_fk_salon_emp;
ALTER TABLE IF EXISTS ONLY public.employees_rewardpenalty DROP CONSTRAINT IF EXISTS employees_rewardpenalty_updated_by_id_5752f4a2_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_rewardpenalty DROP CONSTRAINT IF EXISTS employees_rewardpenalty_created_by_id_67837b43_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_rewardpenalty DROP CONSTRAINT IF EXISTS employees_rewardpena_employee_id_80d8dc3a_fk_employees;
ALTER TABLE IF EXISTS ONLY public.employees_payrollline DROP CONSTRAINT IF EXISTS employees_payrollline_updated_by_id_d372fad4_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_payrollline DROP CONSTRAINT IF EXISTS employees_payrollline_created_by_id_45abb33e_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_payrollline DROP CONSTRAINT IF EXISTS employees_payrolllin_employee_id_d8a4931c_fk_employees;
ALTER TABLE IF EXISTS ONLY public.employees_payrollline DROP CONSTRAINT IF EXISTS employees_payrolllin_batch_id_72f2f128_fk_employees;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbatch_updated_by_id_e5aefed4_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbatch_created_by_id_589f26da_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbatch_branch_id_824ffdfb_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbatch_bank_id_c94e33ae_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbat_ledger_entry_id_9c65139d_fk_salon_fin;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbat_group_id_756cfb89_fk_employees;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetransaction_bank_id_02239859_fk_salon_bank_id;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetr_updated_by_id_c6e097ec_fk_salon_use;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetr_ledger_entry_id_89e218a7_fk_salon_fin;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetr_employee_id_37a3e978_fk_employees;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetr_created_by_id_da6a173c_fk_salon_use;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetr_branch_id_68a6a9cd_fk_salon_bra;
ALTER TABLE IF EXISTS ONLY public.employees_employeegroup DROP CONSTRAINT IF EXISTS employees_employeegroup_updated_by_id_835ee28b_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_employeegroup DROP CONSTRAINT IF EXISTS employees_employeegroup_created_by_id_fc92f23d_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_updated_by_id_546c8556_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_group_id_c5587bba_fk_employees;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_created_by_id_bfa47e39_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_branch_id_16aa717b_fk_salon_branch_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_salon_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.salon_user_username_c7ad3cec_like;
DROP INDEX IF EXISTS public.salon_user_user_permissions_user_id_9b6d5e12;
DROP INDEX IF EXISTS public.salon_user_user_permissions_permission_id_c90b485d;
DROP INDEX IF EXISTS public.salon_user_groups_user_id_094b69f5;
DROP INDEX IF EXISTS public.salon_user_groups_group_id_fe6da36e;
DROP INDEX IF EXISTS public.salon_user_branch_id_3f9bdf84;
DROP INDEX IF EXISTS public.salon_stockmovement_reference_invoice_id_68ee283c;
DROP INDEX IF EXISTS public.salon_stockmovement_reference_consumption_id_819c2b57;
DROP INDEX IF EXISTS public.salon_stockmovement_product_id_d750188e;
DROP INDEX IF EXISTS public.salon_stockmovement_created_by_id_43cfe1db;
DROP INDEX IF EXISTS public.salon_stockmovement_branch_id_f4cd3c25;
DROP INDEX IF EXISTS public.salon_service_category_id_0a191ae7;
DROP INDEX IF EXISTS public.salon_salarypayment_employee_id_6029a968;
DROP INDEX IF EXISTS public.salon_salarypayment_created_by_id_30e722e8;
DROP INDEX IF EXISTS public.salon_salarypayment_branch_id_b7b115a2;
DROP INDEX IF EXISTS public.salon_salarypayment_bank_id_fc228f9f;
DROP INDEX IF EXISTS public.salon_purchaseinvoiceitem_purchase_id_07aadb38;
DROP INDEX IF EXISTS public.salon_purchaseinvoiceitem_product_id_13c22bd7;
DROP INDEX IF EXISTS public.salon_purchaseinvoice_created_by_id_3fa0c4dc;
DROP INDEX IF EXISTS public.salon_purchaseinvoice_branch_id_5450c4b5;
DROP INDEX IF EXISTS public.salon_product_category_id_ac41de83;
DROP INDEX IF EXISTS public.salon_product_branch_id_fdd06562;
DROP INDEX IF EXISTS public.salon_invoiceitem_service_id_9066907a;
DROP INDEX IF EXISTS public.salon_invoiceitem_product_id_79fd85f4;
DROP INDEX IF EXISTS public.salon_invoiceitem_invoice_id_55d43681;
DROP INDEX IF EXISTS public.salon_invoice_customer_id_36323656;
DROP INDEX IF EXISTS public.salon_invoice_created_by_id_96e7d717;
DROP INDEX IF EXISTS public.salon_invoice_branch_id_af606db1;
DROP INDEX IF EXISTS public.salon_invoice_booking_id_cd1bbc2e;
DROP INDEX IF EXISTS public.salon_invoice_barber_id_1bd1ab65;
DROP INDEX IF EXISTS public.salon_invoice_bank_id_1555431b;
DROP INDEX IF EXISTS public.salon_financialledger_created_by_id_f10ff774;
DROP INDEX IF EXISTS public.salon_financialledger_branch_id_7408aafc;
DROP INDEX IF EXISTS public.salon_financialledger_bank_id_e9399aeb;
DROP INDEX IF EXISTS public.salon_expensevoucher_expense_type_id_af93f514;
DROP INDEX IF EXISTS public.salon_expensevoucher_created_by_id_3533d17c;
DROP INDEX IF EXISTS public.salon_expensevoucher_branch_id_c68d0249;
DROP INDEX IF EXISTS public.salon_expensevoucher_bank_id_e66b30dc;
DROP INDEX IF EXISTS public.salon_expensetype_branch_id_48151b1c;
DROP INDEX IF EXISTS public.salon_expensereturn_expense_id_1d1821e9;
DROP INDEX IF EXISTS public.salon_expensereturn_created_by_id_00eb4aba;
DROP INDEX IF EXISTS public.salon_expensereturn_branch_id_53b66006;
DROP INDEX IF EXISTS public.salon_expensereturn_bank_id_4a262084;
DROP INDEX IF EXISTS public.salon_expense_created_by_id_551ba982;
DROP INDEX IF EXISTS public.salon_expense_category_id_65c4dbfd;
DROP INDEX IF EXISTS public.salon_expense_branch_id_098eee01;
DROP INDEX IF EXISTS public.salon_expense_bank_id_8594a1c2;
DROP INDEX IF EXISTS public.salon_employeeadvance_employee_id_b152d06e;
DROP INDEX IF EXISTS public.salon_employeeadvance_deducted_in_id_e54a65cc;
DROP INDEX IF EXISTS public.salon_employeeadvance_created_by_id_5838ec1e;
DROP INDEX IF EXISTS public.salon_employeeadvance_branch_id_51406523;
DROP INDEX IF EXISTS public.salon_employee_branch_id_7437cae7;
DROP INDEX IF EXISTS public.salon_documentcounter_branch_id_1a4031d7;
DROP INDEX IF EXISTS public.salon_dailyqueuenumber_branch_id_ffb4a075;
DROP INDEX IF EXISTS public.salon_customer_branch_id_31e29fd8;
DROP INDEX IF EXISTS public.salon_consumptioninvoiceitem_product_id_906ffb53;
DROP INDEX IF EXISTS public.salon_consumptioninvoiceitem_consumption_id_fe35927a;
DROP INDEX IF EXISTS public.salon_consumptioninvoice_created_by_id_ad81fe2a;
DROP INDEX IF EXISTS public.salon_consumptioninvoice_branch_id_415a54df;
DROP INDEX IF EXISTS public.salon_booking_services_service_id_2a25587b;
DROP INDEX IF EXISTS public.salon_booking_services_booking_id_057e3f36;
DROP INDEX IF EXISTS public.salon_booking_branch_id_160fe177;
DROP INDEX IF EXISTS public.salon_booking_barber_id_ccf3b0b9;
DROP INDEX IF EXISTS public.salon_bank_branch_id_bb0b927c;
DROP INDEX IF EXISTS public.salon_auditlog_user_id_8164f1a3;
DROP INDEX IF EXISTS public.salon_auditlog_branch_id_7f2ca72f;
DROP INDEX IF EXISTS public.salon_advancereturn_created_by_id_e3e7d4b5;
DROP INDEX IF EXISTS public.salon_advancereturn_branch_id_caff267b;
DROP INDEX IF EXISTS public.salon_advancereturn_advance_id_e5e34887;
DROP INDEX IF EXISTS public.employees_rewardpenalty_updated_by_id_5752f4a2;
DROP INDEX IF EXISTS public.employees_rewardpenalty_employee_id_80d8dc3a;
DROP INDEX IF EXISTS public.employees_rewardpenalty_created_by_id_67837b43;
DROP INDEX IF EXISTS public.employees_payrollline_updated_by_id_d372fad4;
DROP INDEX IF EXISTS public.employees_payrollline_employee_id_d8a4931c;
DROP INDEX IF EXISTS public.employees_payrollline_created_by_id_45abb33e;
DROP INDEX IF EXISTS public.employees_payrollline_batch_id_72f2f128;
DROP INDEX IF EXISTS public.employees_payrollbatch_updated_by_id_e5aefed4;
DROP INDEX IF EXISTS public.employees_payrollbatch_ledger_entry_id_9c65139d;
DROP INDEX IF EXISTS public.employees_payrollbatch_group_id_756cfb89;
DROP INDEX IF EXISTS public.employees_payrollbatch_created_by_id_589f26da;
DROP INDEX IF EXISTS public.employees_payrollbatch_branch_id_824ffdfb;
DROP INDEX IF EXISTS public.employees_payrollbatch_bank_id_c94e33ae;
DROP INDEX IF EXISTS public.employees_employeetransaction_updated_by_id_c6e097ec;
DROP INDEX IF EXISTS public.employees_employeetransaction_ledger_entry_id_89e218a7;
DROP INDEX IF EXISTS public.employees_employeetransaction_employee_id_37a3e978;
DROP INDEX IF EXISTS public.employees_employeetransaction_created_by_id_da6a173c;
DROP INDEX IF EXISTS public.employees_employeetransaction_branch_id_68a6a9cd;
DROP INDEX IF EXISTS public.employees_employeetransaction_bank_id_02239859;
DROP INDEX IF EXISTS public.employees_employeegroup_updated_by_id_835ee28b;
DROP INDEX IF EXISTS public.employees_employeegroup_created_by_id_fc92f23d;
DROP INDEX IF EXISTS public.employees_employee_updated_by_id_546c8556;
DROP INDEX IF EXISTS public.employees_employee_phone_cdfc871b_like;
DROP INDEX IF EXISTS public.employees_employee_group_id_c5587bba;
DROP INDEX IF EXISTS public.employees_employee_created_by_id_bfa47e39;
DROP INDEX IF EXISTS public.employees_employee_branch_id_16aa717b;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoice DROP CONSTRAINT IF EXISTS unique_branch_purchase_serial;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS unique_branch_invoice_serial;
ALTER TABLE IF EXISTS ONLY public.salon_expensevoucher DROP CONSTRAINT IF EXISTS unique_branch_expense_voucher_serial;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoice DROP CONSTRAINT IF EXISTS unique_branch_consumption_serial;
ALTER TABLE IF EXISTS ONLY public.salon_user DROP CONSTRAINT IF EXISTS salon_user_username_key;
ALTER TABLE IF EXISTS ONLY public.salon_user_user_permissions DROP CONSTRAINT IF EXISTS salon_user_user_permissions_user_id_permission_id_77565b92_uniq;
ALTER TABLE IF EXISTS ONLY public.salon_user_user_permissions DROP CONSTRAINT IF EXISTS salon_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_user DROP CONSTRAINT IF EXISTS salon_user_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_user_groups DROP CONSTRAINT IF EXISTS salon_user_groups_user_id_group_id_2da4cfaa_uniq;
ALTER TABLE IF EXISTS ONLY public.salon_user_groups DROP CONSTRAINT IF EXISTS salon_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_stockmovement DROP CONSTRAINT IF EXISTS salon_stockmovement_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_service DROP CONSTRAINT IF EXISTS salon_service_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_salonsettings DROP CONSTRAINT IF EXISTS salon_salonsettings_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_salonsettings DROP CONSTRAINT IF EXISTS salon_salonsettings_branch_id_key;
ALTER TABLE IF EXISTS ONLY public.salon_salarypayment DROP CONSTRAINT IF EXISTS salon_salarypayment_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoiceitem DROP CONSTRAINT IF EXISTS salon_purchaseinvoiceitem_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_purchaseinvoice DROP CONSTRAINT IF EXISTS salon_purchaseinvoice_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_product DROP CONSTRAINT IF EXISTS salon_product_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_invoiceitem DROP CONSTRAINT IF EXISTS salon_invoiceitem_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_invoice DROP CONSTRAINT IF EXISTS salon_invoice_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_financialledger DROP CONSTRAINT IF EXISTS salon_financialledger_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_expensevoucher DROP CONSTRAINT IF EXISTS salon_expensevoucher_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_expensetype DROP CONSTRAINT IF EXISTS salon_expensetype_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_expensereturn DROP CONSTRAINT IF EXISTS salon_expensereturn_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_salary_payment_id_key;
ALTER TABLE IF EXISTS ONLY public.salon_expense DROP CONSTRAINT IF EXISTS salon_expense_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_employeeadvance DROP CONSTRAINT IF EXISTS salon_employeeadvance_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_employee DROP CONSTRAINT IF EXISTS salon_employee_user_id_key;
ALTER TABLE IF EXISTS ONLY public.salon_employee DROP CONSTRAINT IF EXISTS salon_employee_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_documentcounter DROP CONSTRAINT IF EXISTS salon_documentcounter_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_documentcounter DROP CONSTRAINT IF EXISTS salon_documentcounter_branch_id_screen_code_date_f7dcac7b_uniq;
ALTER TABLE IF EXISTS ONLY public.salon_dailyqueuenumber DROP CONSTRAINT IF EXISTS salon_dailyqueuenumber_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_dailyqueuenumber DROP CONSTRAINT IF EXISTS salon_dailyqueuenumber_branch_id_date_d6fa7b5b_uniq;
ALTER TABLE IF EXISTS ONLY public.salon_customer DROP CONSTRAINT IF EXISTS salon_customer_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoiceitem DROP CONSTRAINT IF EXISTS salon_consumptioninvoiceitem_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_consumptioninvoice DROP CONSTRAINT IF EXISTS salon_consumptioninvoice_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_category DROP CONSTRAINT IF EXISTS salon_category_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_branch DROP CONSTRAINT IF EXISTS salon_branch_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_booking_services DROP CONSTRAINT IF EXISTS salon_booking_services_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_booking_services DROP CONSTRAINT IF EXISTS salon_booking_services_booking_id_service_id_00b2654b_uniq;
ALTER TABLE IF EXISTS ONLY public.salon_booking DROP CONSTRAINT IF EXISTS salon_booking_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_bank DROP CONSTRAINT IF EXISTS salon_bank_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_auditlog DROP CONSTRAINT IF EXISTS salon_auditlog_pkey;
ALTER TABLE IF EXISTS ONLY public.salon_advancereturn DROP CONSTRAINT IF EXISTS salon_advancereturn_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_rewardpenalty DROP CONSTRAINT IF EXISTS employees_rewardpenalty_serial_key;
ALTER TABLE IF EXISTS ONLY public.employees_rewardpenalty DROP CONSTRAINT IF EXISTS employees_rewardpenalty_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_payrollline DROP CONSTRAINT IF EXISTS employees_payrollline_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbatch_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_payrollbatch DROP CONSTRAINT IF EXISTS employees_payrollbatch_branch_id_group_id_batch_7de88e61_uniq;
ALTER TABLE IF EXISTS ONLY public.employees_employeetransaction DROP CONSTRAINT IF EXISTS employees_employeetransaction_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_employeegroup DROP CONSTRAINT IF EXISTS employees_employeegroup_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_employeegroup DROP CONSTRAINT IF EXISTS employees_employeegroup_code_key;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_pkey;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_phone_key;
ALTER TABLE IF EXISTS ONLY public.employees_employee DROP CONSTRAINT IF EXISTS employees_employee_code_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.salon_user_user_permissions;
DROP TABLE IF EXISTS public.salon_user_groups;
DROP TABLE IF EXISTS public.salon_user;
DROP TABLE IF EXISTS public.salon_stockmovement;
DROP TABLE IF EXISTS public.salon_service;
DROP TABLE IF EXISTS public.salon_salonsettings;
DROP TABLE IF EXISTS public.salon_salarypayment;
DROP TABLE IF EXISTS public.salon_purchaseinvoiceitem;
DROP TABLE IF EXISTS public.salon_purchaseinvoice;
DROP TABLE IF EXISTS public.salon_product;
DROP TABLE IF EXISTS public.salon_invoiceitem;
DROP TABLE IF EXISTS public.salon_invoice;
DROP TABLE IF EXISTS public.salon_financialledger;
DROP TABLE IF EXISTS public.salon_expensevoucher;
DROP TABLE IF EXISTS public.salon_expensetype;
DROP TABLE IF EXISTS public.salon_expensereturn;
DROP TABLE IF EXISTS public.salon_expense;
DROP TABLE IF EXISTS public.salon_employeeadvance;
DROP TABLE IF EXISTS public.salon_employee;
DROP TABLE IF EXISTS public.salon_documentcounter;
DROP TABLE IF EXISTS public.salon_dailyqueuenumber;
DROP TABLE IF EXISTS public.salon_customer;
DROP TABLE IF EXISTS public.salon_consumptioninvoiceitem;
DROP TABLE IF EXISTS public.salon_consumptioninvoice;
DROP TABLE IF EXISTS public.salon_category;
DROP TABLE IF EXISTS public.salon_branch;
DROP TABLE IF EXISTS public.salon_booking_services;
DROP TABLE IF EXISTS public.salon_booking;
DROP TABLE IF EXISTS public.salon_bank;
DROP TABLE IF EXISTS public.salon_auditlog;
DROP TABLE IF EXISTS public.salon_advancereturn;
DROP TABLE IF EXISTS public.employees_rewardpenalty;
DROP TABLE IF EXISTS public.employees_payrollline;
DROP TABLE IF EXISTS public.employees_payrollbatch;
DROP TABLE IF EXISTS public.employees_employeetransaction;
DROP TABLE IF EXISTS public.employees_employeegroup;
DROP TABLE IF EXISTS public.employees_employee;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: employees_employee; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees_employee (
    id bigint NOT NULL,
    code integer NOT NULL,
    name character varying(200) NOT NULL,
    phone character varying(128),
    address character varying(260) NOT NULL,
    hire_date date,
    national_id character varying(20) NOT NULL,
    salary numeric(10,2) NOT NULL,
    commission numeric(10,2) NOT NULL,
    is_active boolean NOT NULL,
    created_at date NOT NULL,
    updated_at date NOT NULL,
    branch_id bigint,
    created_by_id bigint NOT NULL,
    updated_by_id bigint,
    group_id bigint NOT NULL,
    pay_period character varying(10) NOT NULL
);


--
-- Name: employees_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.employees_employee ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employees_employee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employees_employeegroup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees_employeegroup (
    id bigint NOT NULL,
    code integer NOT NULL,
    name character varying(40) NOT NULL,
    created_at date NOT NULL,
    updated_at date NOT NULL,
    created_by_id bigint NOT NULL,
    updated_by_id bigint
);


--
-- Name: employees_employeegroup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.employees_employeegroup ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employees_employeegroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employees_employeetransaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees_employeetransaction (
    id bigint NOT NULL,
    tx_type character varying(20) NOT NULL,
    advance_serial integer NOT NULL,
    payment_serial integer NOT NULL,
    salary_deduct_serial integer NOT NULL,
    date date NOT NULL,
    debit numeric(12,2),
    credit numeric(12,2),
    balance numeric(12,2),
    is_open boolean NOT NULL,
    installment_amount numeric(12,2),
    start_deduct_date date,
    note character varying(120) NOT NULL,
    payment_method character varying(10) NOT NULL,
    created_at date NOT NULL,
    updated_at date NOT NULL,
    bank_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    ledger_entry_id bigint,
    updated_by_id bigint
);


--
-- Name: employees_employeetransaction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.employees_employeetransaction ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employees_employeetransaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employees_payrollbatch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees_payrollbatch (
    id bigint NOT NULL,
    batch_no integer NOT NULL,
    date date NOT NULL,
    payment_method character varying(10) NOT NULL,
    total_bonus numeric(12,2) NOT NULL,
    total_penalty numeric(12,2) NOT NULL,
    total_salary numeric(12,2) NOT NULL,
    total_commission numeric(12,2) NOT NULL,
    total_overtime numeric(12,2) NOT NULL,
    total_adv_sal numeric(12,2) NOT NULL,
    total_adv_fin numeric(12,2) NOT NULL,
    total_net numeric(12,2) NOT NULL,
    is_paid boolean NOT NULL,
    created_at date NOT NULL,
    updated_at date NOT NULL,
    bank_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint NOT NULL,
    group_id bigint NOT NULL,
    ledger_entry_id bigint,
    updated_by_id bigint
);


--
-- Name: employees_payrollbatch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.employees_payrollbatch ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employees_payrollbatch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employees_payrollline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees_payrollline (
    id bigint NOT NULL,
    line_no integer NOT NULL,
    date date NOT NULL,
    bonus numeric(12,2) NOT NULL,
    penalty numeric(12,2) NOT NULL,
    salary numeric(12,2) NOT NULL,
    commission numeric(12,2) NOT NULL,
    overtime numeric(12,2) NOT NULL,
    salary_advance numeric(12,2) NOT NULL,
    advance_deduct numeric(12,2) NOT NULL,
    net_total numeric(12,2) NOT NULL,
    created_at date NOT NULL,
    updated_at date NOT NULL,
    batch_id bigint NOT NULL,
    created_by_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    updated_by_id bigint
);


--
-- Name: employees_payrollline_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.employees_payrollline ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employees_payrollline_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employees_rewardpenalty; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees_rewardpenalty (
    id bigint NOT NULL,
    serial integer NOT NULL,
    date date NOT NULL,
    bonus numeric(12,2),
    penalty numeric(12,2),
    note character varying(40) NOT NULL,
    created_at date NOT NULL,
    updated_at date NOT NULL,
    created_by_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    updated_by_id bigint
);


--
-- Name: employees_rewardpenalty_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.employees_rewardpenalty ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.employees_rewardpenalty_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_advancereturn; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_advancereturn (
    id bigint NOT NULL,
    daily_number integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    advance_id bigint NOT NULL,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    CONSTRAINT salon_advancereturn_daily_number_check CHECK ((daily_number >= 0))
);


--
-- Name: salon_advancereturn_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_advancereturn ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_advancereturn_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_auditlog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_auditlog (
    id bigint NOT NULL,
    action character varying(10) NOT NULL,
    screen_code character varying(10) NOT NULL,
    model_name character varying(50) NOT NULL,
    object_id integer,
    serial_number character varying(30) NOT NULL,
    old_data jsonb NOT NULL,
    new_data jsonb NOT NULL,
    ip_address inet,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint,
    user_id bigint,
    CONSTRAINT salon_auditlog_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: salon_auditlog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_auditlog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_auditlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_bank; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_bank (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    account_number character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint
);


--
-- Name: salon_bank_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_bank ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_bank_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_booking; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_booking (
    id bigint NOT NULL,
    customer_name character varying(100) NOT NULL,
    customer_phone character varying(20) NOT NULL,
    queue_number integer NOT NULL,
    status character varying(20) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    barber_id bigint,
    branch_id bigint NOT NULL,
    serial_number character varying(30) NOT NULL,
    daily_number integer NOT NULL,
    is_vip boolean NOT NULL,
    CONSTRAINT salon_booking_daily_number_check CHECK ((daily_number >= 0)),
    CONSTRAINT salon_booking_queue_number_check CHECK ((queue_number >= 0))
);


--
-- Name: salon_booking_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_booking ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_booking_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_booking_services; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_booking_services (
    id bigint NOT NULL,
    booking_id bigint NOT NULL,
    service_id bigint NOT NULL
);


--
-- Name: salon_booking_services_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_booking_services ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_booking_services_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_branch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_branch (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    address text NOT NULL,
    phone character varying(20) NOT NULL,
    is_main boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: salon_branch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_branch ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_branch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_category (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    type character varying(20) NOT NULL,
    icon character varying(30) NOT NULL,
    color character varying(7) NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: salon_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_category ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_consumptioninvoice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_consumptioninvoice (
    id bigint NOT NULL,
    serial_number integer NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    CONSTRAINT salon_consumptioninvoice_serial_number_check CHECK ((serial_number >= 0))
);


--
-- Name: salon_consumptioninvoice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_consumptioninvoice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_consumptioninvoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_consumptioninvoiceitem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_consumptioninvoiceitem (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    unit_cost numeric(10,2) NOT NULL,
    consumption_id bigint NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT salon_consumptioninvoiceitem_quantity_check CHECK ((quantity >= 0))
);


--
-- Name: salon_consumptioninvoiceitem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_consumptioninvoiceitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_consumptioninvoiceitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_customer (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(254) NOT NULL,
    notes text NOT NULL,
    visits_count integer NOT NULL,
    total_spent numeric(12,2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    CONSTRAINT salon_customer_visits_count_check CHECK ((visits_count >= 0))
);


--
-- Name: salon_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_customer ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_dailyqueuenumber; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_dailyqueuenumber (
    id bigint NOT NULL,
    date date NOT NULL,
    last_number integer NOT NULL,
    branch_id bigint NOT NULL,
    CONSTRAINT salon_dailyqueuenumber_last_number_check CHECK ((last_number >= 0))
);


--
-- Name: salon_dailyqueuenumber_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_dailyqueuenumber ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_dailyqueuenumber_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_documentcounter; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_documentcounter (
    id bigint NOT NULL,
    screen_code character varying(10) NOT NULL,
    date date NOT NULL,
    last_number integer NOT NULL,
    branch_id bigint NOT NULL,
    CONSTRAINT salon_documentcounter_last_number_check CHECK ((last_number >= 0))
);


--
-- Name: salon_documentcounter_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_documentcounter ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_documentcounter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_employee; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_employee (
    id bigint NOT NULL,
    serial_number character varying(30) NOT NULL,
    name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    job_title character varying(50) NOT NULL,
    base_salary numeric(12,2) NOT NULL,
    hire_date date NOT NULL,
    is_active boolean NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    user_id bigint,
    daily_number integer NOT NULL,
    CONSTRAINT salon_employee_daily_number_check CHECK ((daily_number >= 0))
);


--
-- Name: salon_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_employee ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_employee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_employeeadvance; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_employeeadvance (
    id bigint NOT NULL,
    serial_number character varying(30) NOT NULL,
    amount numeric(12,2) NOT NULL,
    notes text NOT NULL,
    is_deducted boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    employee_id bigint NOT NULL,
    deducted_in_id bigint,
    daily_number integer NOT NULL,
    returned_amount numeric(12,2) NOT NULL,
    CONSTRAINT salon_employeeadvance_daily_number_check CHECK ((daily_number >= 0))
);


--
-- Name: salon_employeeadvance_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_employeeadvance ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_employeeadvance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_expense; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_expense (
    id bigint NOT NULL,
    amount numeric(12,2) NOT NULL,
    description text NOT NULL,
    date date NOT NULL,
    receipt character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    category_id bigint,
    created_by_id bigint,
    bank_id bigint,
    payment_method character varying(10) NOT NULL,
    serial_number character varying(30) NOT NULL,
    daily_number integer NOT NULL,
    salary_payment_id bigint,
    CONSTRAINT salon_expense_daily_number_check CHECK ((daily_number >= 0))
);


--
-- Name: salon_expense_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_expense ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_expense_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_expensereturn; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_expensereturn (
    id bigint NOT NULL,
    daily_number integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    payment_method character varying(10) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    bank_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    expense_id bigint NOT NULL,
    CONSTRAINT salon_expensereturn_daily_number_check CHECK ((daily_number >= 0))
);


--
-- Name: salon_expensereturn_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_expensereturn ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_expensereturn_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_expensetype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_expensetype (
    id bigint NOT NULL,
    code character varying(20) NOT NULL,
    name character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL
);


--
-- Name: salon_expensetype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_expensetype ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_expensetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_expensevoucher; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_expensevoucher (
    id bigint NOT NULL,
    voucher_type character varying(10) NOT NULL,
    serial_number integer NOT NULL,
    payment_method character varying(10) NOT NULL,
    amount numeric(12,2) NOT NULL,
    date date NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    bank_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    expense_type_id bigint NOT NULL,
    CONSTRAINT salon_expensevoucher_serial_number_check CHECK ((serial_number >= 0))
);


--
-- Name: salon_expensevoucher_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_expensevoucher ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_expensevoucher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_financialledger; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_financialledger (
    id bigint NOT NULL,
    serial_number character varying(30) NOT NULL,
    screen_code character varying(10) NOT NULL,
    source_id integer,
    reference_serial character varying(30) NOT NULL,
    payment_method character varying(10) NOT NULL,
    direction character varying(3) NOT NULL,
    amount numeric(12,2) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    bank_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    daily_number integer NOT NULL,
    CONSTRAINT salon_financialledger_daily_number_check CHECK ((daily_number >= 0)),
    CONSTRAINT salon_financialledger_source_id_check CHECK ((source_id >= 0))
);


--
-- Name: salon_financialledger_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_financialledger ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_financialledger_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_invoice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_invoice (
    id bigint NOT NULL,
    invoice_number character varying(30) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    discount numeric(10,2) NOT NULL,
    tax numeric(10,2) NOT NULL,
    final_total numeric(12,2) NOT NULL,
    payment_method character varying(10) NOT NULL,
    notes text NOT NULL,
    is_paid boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    bank_id bigint,
    barber_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    customer_id bigint,
    booking_id bigint,
    daily_number integer NOT NULL,
    document_date date,
    is_voided boolean NOT NULL,
    serial_number integer NOT NULL,
    CONSTRAINT salon_invoice_daily_number_check CHECK ((daily_number >= 0)),
    CONSTRAINT salon_invoice_serial_number_check CHECK ((serial_number >= 0))
);


--
-- Name: salon_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_invoice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_invoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_invoiceitem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_invoiceitem (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL,
    total numeric(12,2) NOT NULL,
    invoice_id bigint NOT NULL,
    product_id bigint,
    service_id bigint,
    CONSTRAINT salon_invoiceitem_quantity_check CHECK ((quantity >= 0))
);


--
-- Name: salon_invoiceitem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_invoiceitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_invoiceitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_product; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_product (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(20) NOT NULL,
    price numeric(10,2) NOT NULL,
    cost numeric(10,2) NOT NULL,
    stock integer NOT NULL,
    min_stock integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    category_id bigint,
    CONSTRAINT salon_product_min_stock_check CHECK ((min_stock >= 0)),
    CONSTRAINT salon_product_stock_check CHECK ((stock >= 0))
);


--
-- Name: salon_product_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_product ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_purchaseinvoice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_purchaseinvoice (
    id bigint NOT NULL,
    serial_number integer NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    CONSTRAINT salon_purchaseinvoice_serial_number_check CHECK ((serial_number >= 0))
);


--
-- Name: salon_purchaseinvoice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_purchaseinvoice ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_purchaseinvoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_purchaseinvoiceitem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_purchaseinvoiceitem (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    cost numeric(10,2) NOT NULL,
    price numeric(10,2) NOT NULL,
    product_id bigint NOT NULL,
    purchase_id bigint NOT NULL,
    CONSTRAINT salon_purchaseinvoiceitem_quantity_check CHECK ((quantity >= 0))
);


--
-- Name: salon_purchaseinvoiceitem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_purchaseinvoiceitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_purchaseinvoiceitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_salarypayment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_salarypayment (
    id bigint NOT NULL,
    serial_number character varying(30) NOT NULL,
    amount numeric(12,2) NOT NULL,
    month smallint NOT NULL,
    year smallint NOT NULL,
    payment_method character varying(10) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    bank_id bigint,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    employee_id bigint NOT NULL,
    daily_number integer NOT NULL,
    CONSTRAINT salon_salarypayment_daily_number_check CHECK ((daily_number >= 0)),
    CONSTRAINT salon_salarypayment_month_check CHECK ((month >= 0)),
    CONSTRAINT salon_salarypayment_year_check CHECK ((year >= 0))
);


--
-- Name: salon_salarypayment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_salarypayment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_salarypayment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_salonsettings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_salonsettings (
    id bigint NOT NULL,
    salon_name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    address text NOT NULL,
    currency character varying(10) NOT NULL,
    invoice_header text NOT NULL,
    invoice_footer text NOT NULL,
    whatsapp_footer text NOT NULL,
    receipt_size character varying(10) NOT NULL,
    tax_rate numeric(5,2) NOT NULL,
    auto_backup boolean NOT NULL,
    sms_notifications boolean NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    branch_id bigint,
    logo character varying(100) NOT NULL
);


--
-- Name: salon_salonsettings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_salonsettings ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_salonsettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_service; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_service (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(20) NOT NULL,
    price numeric(10,2) NOT NULL,
    cost numeric(10,2) NOT NULL,
    duration integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    category_id bigint,
    CONSTRAINT salon_service_duration_check CHECK ((duration >= 0))
);


--
-- Name: salon_service_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_service ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_stockmovement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_stockmovement (
    id bigint NOT NULL,
    movement_type character varying(10) NOT NULL,
    quantity integer NOT NULL,
    cost numeric(10,2) NOT NULL,
    notes text NOT NULL,
    date date NOT NULL,
    created_at timestamp with time zone NOT NULL,
    branch_id bigint NOT NULL,
    created_by_id bigint,
    product_id bigint NOT NULL,
    reference_invoice_id bigint,
    serial_number character varying(30) NOT NULL,
    daily_number integer NOT NULL,
    reference_consumption_id bigint,
    CONSTRAINT salon_stockmovement_daily_number_check CHECK ((daily_number >= 0))
);


--
-- Name: salon_stockmovement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_stockmovement ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_stockmovement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    phone character varying(20) NOT NULL,
    photo character varying(100) NOT NULL,
    is_barber boolean NOT NULL,
    commission_rate numeric(5,2),
    can_pos boolean NOT NULL,
    can_inventory boolean NOT NULL,
    can_expenses boolean NOT NULL,
    can_reports boolean NOT NULL,
    can_settings boolean NOT NULL,
    can_users boolean NOT NULL,
    branch_id bigint,
    can_audit boolean NOT NULL,
    can_bookings boolean NOT NULL,
    can_customers boolean NOT NULL,
    can_delete_bookings boolean NOT NULL,
    can_delete_employees boolean NOT NULL,
    can_delete_expenses boolean NOT NULL,
    can_delete_inventory boolean NOT NULL,
    can_delete_pos boolean NOT NULL,
    can_employees boolean NOT NULL,
    can_services boolean NOT NULL
);


--
-- Name: salon_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: salon_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: salon_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.salon_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: salon_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.salon_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.salon_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Branch	8	add_branch
22	Can change Branch	8	change_branch
23	Can delete Branch	8	delete_branch
24	Can view Branch	8	view_branch
25	Can add Category	9	add_category
26	Can change Category	9	change_category
27	Can delete Category	9	delete_category
28	Can view Category	9	view_category
29	Can add User	17	add_user
30	Can change User	17	change_user
31	Can delete User	17	delete_user
32	Can view User	17	view_user
33	Can add Bank	6	add_bank
34	Can change Bank	6	change_bank
35	Can delete Bank	6	delete_bank
36	Can view Bank	6	view_bank
37	Can add Customer	10	add_customer
38	Can change Customer	10	change_customer
39	Can delete Customer	10	delete_customer
40	Can view Customer	10	view_customer
41	Can add Expense	11	add_expense
42	Can change Expense	11	change_expense
43	Can delete Expense	11	delete_expense
44	Can view Expense	11	view_expense
45	Can add Invoice	12	add_invoice
46	Can change Invoice	12	change_invoice
47	Can delete Invoice	12	delete_invoice
48	Can view Invoice	12	view_invoice
49	Can add Product	14	add_product
50	Can change Product	14	change_product
51	Can delete Product	14	delete_product
52	Can view Product	14	view_product
53	Can add Service	15	add_service
54	Can change Service	15	change_service
55	Can delete Service	15	delete_service
56	Can view Service	15	view_service
57	Can add Invoice Item	13	add_invoiceitem
58	Can change Invoice Item	13	change_invoiceitem
59	Can delete Invoice Item	13	delete_invoiceitem
60	Can view Invoice Item	13	view_invoiceitem
61	Can add Booking	7	add_booking
62	Can change Booking	7	change_booking
63	Can delete Booking	7	delete_booking
64	Can view Booking	7	view_booking
65	Can add Stock Movement	16	add_stockmovement
66	Can change Stock Movement	16	change_stockmovement
67	Can delete Stock Movement	16	delete_stockmovement
68	Can view Stock Movement	16	view_stockmovement
69	Can add رقم الدور اليومي	18	add_dailyqueuenumber
70	Can change رقم الدور اليومي	18	change_dailyqueuenumber
71	Can delete رقم الدور اليومي	18	delete_dailyqueuenumber
72	Can view رقم الدور اليومي	18	view_dailyqueuenumber
73	Can add Audit Log	19	add_auditlog
74	Can change Audit Log	19	change_auditlog
75	Can delete Audit Log	19	delete_auditlog
76	Can view Audit Log	19	view_auditlog
77	Can add Employee	21	add_employee
78	Can change Employee	21	change_employee
79	Can delete Employee	21	delete_employee
80	Can view Employee	21	view_employee
81	Can add Ledger Entry	23	add_financialledger
82	Can change Ledger Entry	23	change_financialledger
83	Can delete Ledger Entry	23	delete_financialledger
84	Can view Ledger Entry	23	view_financialledger
85	Can add Salary Payment	24	add_salarypayment
86	Can change Salary Payment	24	change_salarypayment
87	Can delete Salary Payment	24	delete_salarypayment
88	Can view Salary Payment	24	view_salarypayment
89	Can add Employee Advance	22	add_employeeadvance
90	Can change Employee Advance	22	change_employeeadvance
91	Can delete Employee Advance	22	delete_employeeadvance
92	Can view Employee Advance	22	view_employeeadvance
93	Can add Settings	25	add_salonsettings
94	Can change Settings	25	change_salonsettings
95	Can delete Settings	25	delete_salonsettings
96	Can view Settings	25	view_salonsettings
97	Can add Serial Counter	20	add_documentcounter
98	Can change Serial Counter	20	change_documentcounter
99	Can delete Serial Counter	20	delete_documentcounter
100	Can view Serial Counter	20	view_documentcounter
101	Can add Advance Return	26	add_advancereturn
102	Can change Advance Return	26	change_advancereturn
103	Can delete Advance Return	26	delete_advancereturn
104	Can view Advance Return	26	view_advancereturn
105	Can add Expense Return	27	add_expensereturn
106	Can change Expense Return	27	change_expensereturn
107	Can delete Expense Return	27	delete_expensereturn
108	Can view Expense Return	27	view_expensereturn
109	Can add دفعة مرتبات	31	add_payrollbatch
110	Can change دفعة مرتبات	31	change_payrollbatch
111	Can delete دفعة مرتبات	31	delete_payrollbatch
112	Can view دفعة مرتبات	31	view_payrollbatch
113	Can add موظف	28	add_employee
114	Can change موظف	28	change_employee
115	Can delete موظف	28	delete_employee
116	Can view موظف	28	view_employee
117	Can add مكافأة/جزاء	33	add_rewardpenalty
118	Can change مكافأة/جزاء	33	change_rewardpenalty
119	Can delete مكافأة/جزاء	33	delete_rewardpenalty
120	Can view مكافأة/جزاء	33	view_rewardpenalty
121	Can add حركة موظف	30	add_employeetransaction
122	Can change حركة موظف	30	change_employeetransaction
123	Can delete حركة موظف	30	delete_employeetransaction
124	Can view حركة موظف	30	view_employeetransaction
125	Can add بند مرتب	32	add_payrollline
126	Can change بند مرتب	32	change_payrollline
127	Can delete بند مرتب	32	delete_payrollline
128	Can view بند مرتب	32	view_payrollline
129	Can add مجموعة موظفين	29	add_employeegroup
130	Can change مجموعة موظفين	29	change_employeegroup
131	Can delete مجموعة موظفين	29	delete_employeegroup
132	Can view مجموعة موظفين	29	view_employeegroup
133	Can add Purchase Invoice	34	add_purchaseinvoice
134	Can change Purchase Invoice	34	change_purchaseinvoice
135	Can delete Purchase Invoice	34	delete_purchaseinvoice
136	Can view Purchase Invoice	34	view_purchaseinvoice
137	Can add Purchase Item	35	add_purchaseinvoiceitem
138	Can change Purchase Item	35	change_purchaseinvoiceitem
139	Can delete Purchase Item	35	delete_purchaseinvoiceitem
140	Can view Purchase Item	35	view_purchaseinvoiceitem
141	Can add Consumption Invoice	36	add_consumptioninvoice
142	Can change Consumption Invoice	36	change_consumptioninvoice
143	Can delete Consumption Invoice	36	delete_consumptioninvoice
144	Can view Consumption Invoice	36	view_consumptioninvoice
145	Can add Consumption Item	37	add_consumptioninvoiceitem
146	Can change Consumption Item	37	change_consumptioninvoiceitem
147	Can delete Consumption Item	37	delete_consumptioninvoiceitem
148	Can view Consumption Item	37	view_consumptioninvoiceitem
149	Can add Expense Type	38	add_expensetype
150	Can change Expense Type	38	change_expensetype
151	Can delete Expense Type	38	delete_expensetype
152	Can view Expense Type	38	view_expensetype
153	Can add Expense Voucher	39	add_expensevoucher
154	Can change Expense Voucher	39	change_expensevoucher
155	Can delete Expense Voucher	39	delete_expensevoucher
156	Can view Expense Voucher	39	view_expensevoucher
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	salon	bank
7	salon	booking
8	salon	branch
9	salon	category
10	salon	customer
11	salon	expense
12	salon	invoice
13	salon	invoiceitem
14	salon	product
15	salon	service
16	salon	stockmovement
17	salon	user
18	salon	dailyqueuenumber
19	salon	auditlog
20	salon	documentcounter
21	salon	employee
22	salon	employeeadvance
23	salon	financialledger
24	salon	salarypayment
25	salon	salonsettings
26	salon	advancereturn
27	salon	expensereturn
28	employees	employee
29	employees	employeegroup
30	employees	employeetransaction
31	employees	payrollbatch
32	employees	payrollline
33	employees	rewardpenalty
34	salon	purchaseinvoice
35	salon	purchaseinvoiceitem
36	salon	consumptioninvoice
37	salon	consumptioninvoiceitem
38	salon	expensetype
39	salon	expensevoucher
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-05-18 02:20:21.563494+03
2	contenttypes	0002_remove_content_type_name	2026-05-18 02:20:21.581845+03
3	auth	0001_initial	2026-05-18 02:20:21.664102+03
4	auth	0002_alter_permission_name_max_length	2026-05-18 02:20:21.677001+03
5	auth	0003_alter_user_email_max_length	2026-05-18 02:20:21.687672+03
6	auth	0004_alter_user_username_opts	2026-05-18 02:20:21.699014+03
7	auth	0005_alter_user_last_login_null	2026-05-18 02:20:21.711078+03
8	auth	0006_require_contenttypes_0002	2026-05-18 02:20:21.713457+03
9	auth	0007_alter_validators_add_error_messages	2026-05-18 02:20:21.723031+03
10	auth	0008_alter_user_username_max_length	2026-05-18 02:20:21.735732+03
11	auth	0009_alter_user_last_name_max_length	2026-05-18 02:20:21.746539+03
12	auth	0010_alter_group_name_max_length	2026-05-18 02:20:21.760603+03
13	auth	0011_update_proxy_permissions	2026-05-18 02:20:21.772047+03
14	auth	0012_alter_user_first_name_max_length	2026-05-18 02:20:21.785055+03
15	salon	0001_initial	2026-05-18 02:20:22.266941+03
16	admin	0001_initial	2026-05-18 02:20:22.327481+03
17	admin	0002_logentry_remove_auto_add	2026-05-18 02:20:22.349805+03
18	admin	0003_logentry_add_action_flag_choices	2026-05-18 02:20:22.380771+03
19	salon	0002_remove_service_branch	2026-05-18 02:20:22.457852+03
20	sessions	0001_initial	2026-05-18 02:20:22.478782+03
21	salon	0003_dailyqueuenumber	2026-05-30 06:10:06.821594+03
22	salon	0004_booking_serial_number_expense_bank_and_more	2026-06-17 03:31:14.5629+03
23	salon	0005_booking_daily_number_employee_daily_number_and_more	2026-06-17 17:07:53.133293+03
24	employees	0001_initial	2026-06-17 18:56:11.946758+03
25	employees	0002_employee_pay_period_simplify	2026-06-18 01:45:11.966427+03
26	salon	0004_invoice_serial_number	2026-06-18 02:15:59.15049+03
27	salon	0005_invoice_daily_number	2026-06-18 02:24:00.495397+03
28	salon	0006_booking_is_vip	2026-06-18 02:52:38.173728+03
29	salon	0007_booking_serial_number	2026-06-18 03:01:45.215157+03
30	salon	0008_purchaseinvoice	2026-06-18 03:15:34.560949+03
31	salon	0009_stockmovement_serial	2026-06-18 03:39:59.302664+03
32	salon	0010_consumptioninvoice	2026-06-18 03:55:44.560776+03
33	salon	0011_expensetype_expensevoucher	2026-06-18 04:07:59.022949+03
34	salon	0012_salonsettings	2026-06-18 19:30:17.096979+03
35	salon	0013_salonsettings_logo	2026-06-18 19:32:18.416576+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
c6oi3yjx2y0qfs0p3m7pyb7oc3i80zz3	.eJxVjMsKwjAQAP9lzxLyWLJNj979hpDHrqlKC017Ev9dCj3odWaYN8S0by3undc4VRjBwOWX5VSePB-iPtJ8X1RZ5m2dsjoSddqubkvl1_Vs_wYt9QYjCLJYZG_ICDnySZyvEnQlQXIVg2WxDgetM9mCIQS0Q3JEmor3nOHzBdeiNzQ:1wOuAw:2GBVqsux5RBr10DnfMKXMYkVe45fFviQtTbXGfrv6cg	2026-06-01 12:22:14.308686+03
yzn7re4gg0889a8qo52e822iqtjnzwel	.eJxVjMsKwjAQAP9lzxLyWLJNj979hpDHrqlKC017Ev9dCj3odWaYN8S0by3undc4VRjBwOWX5VSePB-iPtJ8X1RZ5m2dsjoSddqubkvl1_Vs_wYt9QYjCLJYZG_ICDnySZyvEnQlQXIVg2WxDgetM9mCIQS0Q3JEmor3nOHzBdeiNzQ:1wTBY5:qHUI7RoK7MJ4NuxSw1ow0meWxe1ha0b8MkKF2ndsAg4	2026-06-13 07:43:49.438281+03
yeju8z6wm1goquuns6hgaj9lovbnk61q	.eJxVjMsKwjAQAP9lzxLyWLJNj979hpDHrqlKC017Ev9dCj3odWaYN8S0by3undc4VRjBwOWX5VSePB-iPtJ8X1RZ5m2dsjoSddqubkvl1_Vs_wYt9QYjCLJYZG_ICDnySZyvEnQlQXIVg2WxDgetM9mCIQS0Q3JEmor3nOHzBdeiNzQ:1wV6tK:TA_geJSE8Pt9__gdd65GRHV9zbYcb1cWkhdEMIXt8SA	2026-06-18 15:09:42.287631+03
5zrqy3hxnn6kgu4ecivfmwatrv6ovytq	.eJxVjMsKwjAQAP9lzxLyWLJNj979hpDHrqlKC017Ev9dCj3odWaYN8S0by3undc4VRjBwOWX5VSePB-iPtJ8X1RZ5m2dsjoSddqubkvl1_Vs_wYt9QYjCLJYZG_ICDnySZyvEnQlQXIVg2WxDgetM9mCIQS0Q3JEmor3nOHzBdeiNzQ:1wWydI:CWOWwgX79TIr8FWNdW_GVjns--J5Th_xv0_nqfK0QJ4	2026-06-23 18:44:52.759786+03
2w6w20wt9yoq5w2wtdgum3s4si13cy96	.eJxVjMsKwjAQAP9lzxLyWLJNj979hpDHrqlKC017Ev9dCj3odWaYN8S0by3undc4VRjBwOWX5VSePB-iPtJ8X1RZ5m2dsjoSddqubkvl1_Vs_wYt9QYjCLJYZG_ICDnySZyvEnQlQXIVg2WxDgetM9mCIQS0Q3JEmor3nOHzBdeiNzQ:1wZ6Ap:0ymOhlKl99USE56dpyXhtzSVOCvfA-1PAF2GfeuVtmI	2026-06-29 15:12:15.575516+03
t52vtqf28y6o4abacjle5xs90a5mn0zy	.eJxVjMsKwjAQAP9lzxLyWLJNj979hpDHrqlKC017Ev9dCj3odWaYN8S0by3undc4VRjBwOWX5VSePB-iPtJ8X1RZ5m2dsjoSddqubkvl1_Vs_wYt9QYjCLJYZG_ICDnySZyvEnQlQXIVg2WxDgetM9mCIQS0Q3JEmor3nOHzBdeiNzQ:1wZshu:BMxgkuwit7mMExHN6L42DSiQv5xc37nO6GEP-S20Gr8	2026-07-01 19:01:38.490491+03
lyeozkd9912g2il7mls3g4lw1ebomx8x	.eJxVjMsOwiAQAP-FsyG8SlmP3vsNZGEXWzWQlPZk_HfTpAe9zkzmLSLu2xz3zmtcSFyFFpdfljA_uR6CHljvTeZWt3VJ8kjkabucGvHrdrZ_gxn7fGy9KiN5m5UNfuRhZNSQnXXFAOSA2hYHpmg0KQUPQMPAihybYEi7VMTnC8qeN4I:1wZu1A:psj8I3VWAz4VO4gnreN-Rz2AZ-2NXvFuIGUt1EK0pDs	2026-07-01 20:25:36.18379+03
hlerrzs2xgkr14ek66kk4xut9epc582w	.eJxVjDkOwjAQAP-yNbLs-MhR0vMGa6-QAIqlOKkQf0eRUkA7M5o3ZNy3Ke9V1zwLDODg8ssI-anLIeSBy70YLsu2zmSOxJy2mlsRfV3P9m8wYZ1gANIkseXRcR_GLrnYqUq0Kuy1RcZkgwQi9I4Jx9RGhx0JN8S-6W0f4PMFGB05Fw:1wZyW0:E9hwty2wcxMneHvew9UhrYIzMUuYzqNY4nSo09vzZcA	2026-07-02 01:13:44.514261+03
3scsuadb4yge5c6jlmwkh26mmnbk1jxq	.eJxVjDEOgzAMAP_iuYpinNCEsTtvQHYSF9oKJAJT1b9XSAztene6Nwy8b-Ow17IOU4YOEC6_TDg9y3yI_OD5vpi0zNs6iTkSc9pq-iWX1-1s_wYj1xE6EFuoaQNGRcyUY8weNdhiKZGgS06ctpJQ2V5FtA3ktTTqIgVC9hY-X974N8U:1wZyWA:puFkWz9FKI1r5mA8075z9axYjWeOGtUafEMcjvHxBxc	2026-07-02 01:13:54.332434+03
t14r6hovoktncu59ciifetm86l6mio66	.eJxVjDEOgzAMAP_iuYpinNCEsTtvQHYSF9oKJAJT1b9XSAztene6Nwy8b-Ow17IOU4YOEC6_TDg9y3yI_OD5vpi0zNs6iTkSc9pq-iWX1-1s_wYj1xE6EFuoaQNGRcyUY8weNdhiKZGgS06ctpJQ2V5FtA3ktTTqIgVC9hY-X974N8U:1wZzoj:h67tdQNetvFcmcbTLOUthiA_R23IlDjYz0WIhsl-bPA	2026-07-02 02:37:09.468176+03
iptqs0ojqmc4waorjguyal7ty1tn8883	.eJxVjDEOgzAMAP_iuYpinNCEsTtvQHYSF9oKJAJT1b9XSAztene6Nwy8b-Ow17IOU4YOEC6_TDg9y3yI_OD5vpi0zNs6iTkSc9pq-iWX1-1s_wYj1xE6EFuoaQNGRcyUY8weNdhiKZGgS06ctpJQ2V5FtA3ktTTqIgVC9hY-X974N8U:1wa0cx:DCUhUzJ_vb0go7h--ZcjRQXAXHjMQi7DaqXzraLDN38	2026-07-02 03:29:03.40514+03
h1ygi3nbzgcsrheqysb61k91ljkp4mdf	.eJxVjDEOgzAMAP_iuYpinNCEsTtvQHYSF9oKJAJT1b9XSAztene6Nwy8b-Ow17IOU4YOEC6_TDg9y3yI_OD5vpi0zNs6iTkSc9pq-iWX1-1s_wYj1xE6EFuoaQNGRcyUY8weNdhiKZGgS06ctpJQ2V5FtA3ktTTqIgVC9hY-X974N8U:1wa0oB:dokg_TPxrVHiQyO3zlIHnjwekcFdJOyfmyzhOEDX9EI	2026-07-02 03:40:39.772122+03
\.


--
-- Data for Name: employees_employee; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.employees_employee (id, code, name, phone, address, hire_date, national_id, salary, commission, is_active, created_at, updated_at, branch_id, created_by_id, updated_by_id, group_id, pay_period) FROM stdin;
1	1	m	0	,km	2026-06-17	LEG000001	1000.00	0.00	t	2026-06-17	2026-06-17	2	1	\N	1	monthly
\.


--
-- Data for Name: employees_employeegroup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.employees_employeegroup (id, code, name, created_at, updated_at, created_by_id, updated_by_id) FROM stdin;
1	1	عام	2026-06-17	2026-06-17	1	\N
\.


--
-- Data for Name: employees_employeetransaction; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.employees_employeetransaction (id, tx_type, advance_serial, payment_serial, salary_deduct_serial, date, debit, credit, balance, is_open, installment_amount, start_deduct_date, note, payment_method, created_at, updated_at, bank_id, branch_id, created_by_id, employee_id, ledger_entry_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: employees_payrollbatch; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.employees_payrollbatch (id, batch_no, date, payment_method, total_bonus, total_penalty, total_salary, total_commission, total_overtime, total_adv_sal, total_adv_fin, total_net, is_paid, created_at, updated_at, bank_id, branch_id, created_by_id, group_id, ledger_entry_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: employees_payrollline; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.employees_payrollline (id, line_no, date, bonus, penalty, salary, commission, overtime, salary_advance, advance_deduct, net_total, created_at, updated_at, batch_id, created_by_id, employee_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: employees_rewardpenalty; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.employees_rewardpenalty (id, serial, date, bonus, penalty, note, created_at, updated_at, created_by_id, employee_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: salon_advancereturn; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_advancereturn (id, daily_number, amount, notes, created_at, advance_id, branch_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: salon_auditlog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_auditlog (id, action, screen_code, model_name, object_id, serial_number, old_data, new_data, ip_address, created_at, branch_id, user_id) FROM stdin;
1	create	POS	Invoice	30	POS-2-20260617-0001	{}	{"id": 30, "tax": 0, "bank": null, "notes": "", "barber": null, "branch": 2, "booking": null, "is_paid": true, "customer": 3, "discount": "0", "subtotal": 0, "created_at": "2026-06-17T00:41:28.186896+00:00", "created_by": 1, "final_total": "0", "invoice_number": "POS-2-20260617-0001", "payment_method": "cash"}	\N	2026-06-17 03:41:28.195397+03	2	1
2	create	STK	StockMovement	1	STK-2-20260617-0001	{}	{"id": 1, "cost": "90", "date": "2026-06-17", "notes": "", "branch": 2, "product": 1, "quantity": 2, "created_at": "2026-06-17T00:43:55.221830+00:00", "created_by": 1, "movement_type": "out", "serial_number": "STK-2-20260617-0001", "reference_invoice": null}	\N	2026-06-17 03:43:55.267788+03	2	1
3	create	EMP	Employee	1	EMP-2-20260617-0001	{}	{"id": 1, "name": "m", "user": null, "notes": ",km", "phone": "0", "branch": 2, "hire_date": "2026-06-17", "is_active": true, "job_title": "kk", "created_at": "2026-06-17T00:45:45.377529+00:00", "base_salary": "1000", "serial_number": "EMP-2-20260617-0001"}	\N	2026-06-17 03:45:45.404585+03	2	\N
4	create	SAL	SalaryPayment	1	SAL-2-20260617-0001	{}	{"id": 1, "bank": null, "year": 2026, "month": 6, "notes": "", "amount": "200", "branch": 2, "employee": 1, "created_at": "2026-06-17T00:46:36.574146+00:00", "created_by": 1, "serial_number": "SAL-2-20260617-0001", "payment_method": "cash"}	\N	2026-06-17 03:46:36.629485+03	2	1
5	create	POS	Invoice	31	2	{}	{"id": 31, "tax": 0, "bank": null, "notes": "", "barber": null, "branch": 2, "booking": null, "is_paid": true, "customer": 6, "discount": "0", "subtotal": 0, "is_voided": false, "created_at": "2026-06-17T14:12:47.349314+00:00", "created_by": 1, "final_total": "0", "daily_number": 2, "document_date": "2026-06-17", "invoice_number": "2-20260617-0002", "payment_method": "cash"}	\N	2026-06-17 17:12:47.353471+03	2	1
6	create	POS	Invoice	32	3	{}	{"id": 32, "tax": 0, "bank": null, "notes": "", "barber": null, "branch": 2, "booking": null, "is_paid": true, "customer": 7, "discount": "0", "subtotal": 0, "is_voided": false, "created_at": "2026-06-17T14:15:53.288872+00:00", "created_by": 1, "final_total": "0", "daily_number": 3, "document_date": "2026-06-17", "invoice_number": "2-20260617-0003", "payment_method": "cash"}	\N	2026-06-17 17:15:53.292724+03	2	1
7	create	BKG	Booking	5	1	{}	{"id": 5, "notes": "", "barber": null, "branch": 2, "status": "waiting", "created_at": "2026-06-17T16:34:49.397345+00:00", "started_at": null, "completed_at": null, "daily_number": 1, "queue_number": 1, "customer_name": "ghf", "serial_number": "1", "customer_phone": "45"}	\N	2026-06-17 19:34:49.523149+03	2	\N
\.


--
-- Data for Name: salon_bank; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_bank (id, name, account_number, is_active, created_at, branch_id) FROM stdin;
\.


--
-- Data for Name: salon_booking; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_booking (id, customer_name, customer_phone, queue_number, status, notes, created_at, started_at, completed_at, barber_id, branch_id, serial_number, daily_number, is_vip) FROM stdin;
1	asdfasd	98	1	cancelled	999	2026-05-18 03:25:24.985979+03	2026-05-18 03:38:38.33802+03	2026-05-18 12:20:56.836973+03	\N	2	1	1	f
3	kljkl	098765	1	completed	lkjh	2026-05-30 06:11:05.122313+03	2026-05-30 06:17:13.40758+03	2026-05-30 06:17:14.982451+03	\N	2	1	1	f
4	;mlkjnbhg	09876	1	in_progress	klj	2026-05-31 04:47:50.469548+03	2026-06-03 19:07:23.604267+03	\N	\N	2	1	1	f
5	ghf	45	1	waiting		2026-06-17 19:34:49.397345+03	\N	\N	\N	2	1	1	f
2	بيسب	3434	2	waiting	يس	2026-05-18 03:38:51.247189+03	\N	\N	\N	2	2	2	f
8	نايل	01029029992	1	completed	ة	2026-06-18 03:04:26.163476+03	2026-06-18 03:05:08.535754+03	2026-06-18 03:05:08.535748+03	\N	2	1	1	t
\.


--
-- Data for Name: salon_booking_services; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_booking_services (id, booking_id, service_id) FROM stdin;
2	8	1
3	8	4
\.


--
-- Data for Name: salon_branch; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_branch (id, name, address, phone, is_main, is_active, created_at) FROM stdin;
2	Head Office	0	0	t	t	2026-05-18 00:00:00+03
3	Nasr City	0	0	f	t	2026-05-18 00:00:00+03
4	korba	0	0	f	t	2026-05-18 00:00:00+03
\.


--
-- Data for Name: salon_category; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_category (id, name, type, icon, color, is_active) FROM stdin;
\.


--
-- Data for Name: salon_consumptioninvoice; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_consumptioninvoice (id, serial_number, notes, created_at, branch_id, created_by_id) FROM stdin;
1	1		2026-06-18 03:58:16.779942+03	2	1
\.


--
-- Data for Name: salon_consumptioninvoiceitem; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_consumptioninvoiceitem (id, quantity, unit_cost, consumption_id, product_id) FROM stdin;
1	5	100.00	1	2
\.


--
-- Data for Name: salon_customer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_customer (id, name, phone, email, notes, visits_count, total_spent, created_at, branch_id) FROM stdin;
2	dfgsfad	4321			1	300.00	2026-05-18 12:20:43.25864+03	2
1	محمد	01116059950			10	2560.00	2026-05-18 03:37:41.209637+03	2
4	يسب	3			1	77.00	2026-06-03 19:01:45.19315+03	2
5	نم	0			1	180.00	2026-06-16 04:08:23.060325+03	2
6	fg	fg			1	160.00	2026-06-17 17:12:47.324757+03	2
7	jkhgjfhg	123456			1	220.00	2026-06-17 17:15:53.278939+03	2
11	010	010			1	180.00	2026-06-18 02:24:15.048027+03	2
10	محمد	011			0	0.00	2026-06-18 02:23:57.071223+03	2
12	نم				1	180.00	2026-06-18 02:35:51.013993+03	2
13	9	9			1	180.00	2026-06-18 02:36:06.334659+03	2
14	نمن	456789			0	0.00	2026-06-18 02:38:41.70881+03	2
3	نتلاا	01029029992			16	2610.00	2026-05-30 06:25:40.944937+03	2
15	نمت	3456			1	600.00	2026-06-18 02:42:00.727312+03	2
\.


--
-- Data for Name: salon_dailyqueuenumber; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_dailyqueuenumber (id, date, last_number, branch_id) FROM stdin;
2	2026-05-30	1	4
1	2026-05-30	10	2
4	2026-06-03	47	2
5	2026-06-04	1	2
3	2026-05-31	4	2
6	2026-06-09	1	2
7	2026-06-17	5	2
8	2026-06-18	5	2
\.


--
-- Data for Name: salon_documentcounter; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_documentcounter (id, screen_code, date, last_number, branch_id) FROM stdin;
3	STK	2026-06-17	1	2
4	EMP	2026-06-17	1	2
5	SAL	2026-06-17	1	2
1	POS	2026-06-17	3	2
2	CSH	2026-06-17	4	2
6	BKG	2026-06-17	1	2
\.


--
-- Data for Name: salon_employee; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_employee (id, serial_number, name, phone, job_title, base_salary, hire_date, is_active, notes, created_at, branch_id, user_id, daily_number) FROM stdin;
1	EMP-2-20260617-0001	m	0	kk	1000.00	2026-06-17	t	,km	2026-06-17 03:45:45.377529+03	2	\N	0
\.


--
-- Data for Name: salon_employeeadvance; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_employeeadvance (id, serial_number, amount, notes, is_deducted, created_at, branch_id, created_by_id, employee_id, deducted_in_id, daily_number, returned_amount) FROM stdin;
\.


--
-- Data for Name: salon_expense; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_expense (id, amount, description, date, receipt, created_at, branch_id, category_id, created_by_id, bank_id, payment_method, serial_number, daily_number, salary_payment_id) FROM stdin;
1	8.00	m,,	2026-05-26		2026-05-26 22:44:24.300971+03	2	\N	1	\N	cash		0	\N
\.


--
-- Data for Name: salon_expensereturn; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_expensereturn (id, daily_number, amount, payment_method, notes, created_at, bank_id, branch_id, created_by_id, expense_id) FROM stdin;
\.


--
-- Data for Name: salon_expensetype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_expensetype (id, code, name, is_active, created_at, branch_id) FROM stdin;
1	1	سي	t	2026-06-18 04:09:10.065182+03	2
\.


--
-- Data for Name: salon_expensevoucher; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_expensevoucher (id, voucher_type, serial_number, payment_method, amount, date, notes, created_at, bank_id, branch_id, created_by_id, expense_type_id) FROM stdin;
1	out	1	cash	5000.00	2026-06-18		2026-06-18 04:09:45.285091+03	\N	2	1	1
2	return	1	cash	500.00	2026-06-18		2026-06-18 04:10:24.688216+03	\N	2	1	1
\.


--
-- Data for Name: salon_financialledger; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_financialledger (id, serial_number, screen_code, source_id, reference_serial, payment_method, direction, amount, description, created_at, bank_id, branch_id, created_by_id, daily_number) FROM stdin;
1	CSH-2-20260617-0001	POS	30	POS-2-20260617-0001	cash	in	0.00	فاتورة بيع POS-2-20260617-0001	2026-06-17 03:41:28.217732+03	\N	2	1	0
2	CSH-2-20260617-0002	SAL	1	SAL-2-20260617-0001	cash	out	200.00	مرتب m - SAL-2-20260617-0001	2026-06-17 03:46:36.648361+03	\N	2	1	0
3	3	POS	31	2	cash	in	0.00	فاتورة بيع #2	2026-06-17 17:12:47.363448+03	\N	2	1	3
4	4	POS	32	3	cash	in	0.00	فاتورة بيع #3	2026-06-17 17:15:53.30039+03	\N	2	1	4
\.


--
-- Data for Name: salon_invoice; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_invoice (id, invoice_number, subtotal, discount, tax, final_total, payment_method, notes, is_paid, created_at, bank_id, barber_id, branch_id, created_by_id, customer_id, booking_id, daily_number, document_date, is_voided, serial_number) FROM stdin;
32	32	220.00	0.00	0.00	220.00	cash		t	2026-06-17 17:15:53.288872+03	\N	\N	2	1	7	\N	32	2026-06-17	f	32
31	31	160.00	0.00	0.00	160.00	cash		t	2026-06-17 17:12:47.349314+03	\N	\N	2	1	6	\N	31	2026-06-17	f	31
30	30	180.00	0.00	0.00	180.00	cash		t	2026-06-17 03:41:28.186896+03	\N	\N	2	1	3	\N	30	2026-06-17	f	30
29	29	180.00	0.00	0.00	180.00	cash		t	2026-06-16 04:08:23.117403+03	\N	\N	2	1	5	\N	29	2026-06-16	f	29
28	28	80.00	3.00	0.00	77.00	cash		t	2026-06-03 19:01:45.242941+03	\N	\N	2	1	4	\N	28	2026-06-03	f	28
27	27	100.00	0.00	0.00	100.00	cash		t	2026-05-31 06:19:22.319427+03	\N	\N	2	1	3	\N	27	2026-05-31	f	27
26	26	80.00	0.00	0.00	80.00	cash		t	2026-05-31 06:16:50.16498+03	\N	\N	2	1	1	\N	26	2026-05-31	f	26
25	25	100.00	0.00	0.00	100.00	cash		t	2026-05-31 06:13:10.099024+03	\N	\N	2	1	1	\N	25	2026-05-31	f	25
24	24	100.00	0.00	0.00	100.00	cash		t	2026-05-31 06:07:21.85863+03	\N	\N	2	1	1	\N	24	2026-05-31	f	24
23	23	100.00	0.00	0.00	100.00	cash		t	2026-05-31 06:05:44.166837+03	\N	\N	2	1	1	\N	23	2026-05-31	f	23
22	22	80.00	0.00	0.00	80.00	cash		t	2026-05-31 06:04:40.615952+03	\N	\N	2	1	3	\N	22	2026-05-31	f	22
21	21	100.00	0.00	0.00	100.00	cash		t	2026-05-31 06:03:50.523428+03	\N	\N	2	1	3	\N	21	2026-05-31	f	21
20	20	80.00	0.00	0.00	80.00	cash		t	2026-05-31 05:43:04.095488+03	\N	\N	2	1	3	\N	20	2026-05-31	f	20
19	19	120.00	0.00	0.00	120.00	cash		t	2026-05-31 05:35:17.897751+03	\N	\N	2	1	3	\N	19	2026-05-31	f	19
18	18	120.00	0.00	0.00	120.00	cash		t	2026-05-31 05:34:43.152613+03	\N	\N	2	1	3	\N	18	2026-05-31	f	18
17	17	120.00	0.00	0.00	120.00	cash		t	2026-05-31 05:34:02.939334+03	\N	\N	2	1	3	\N	17	2026-05-31	f	17
16	16	120.00	0.00	0.00	120.00	cash		t	2026-05-31 05:31:32.562987+03	\N	\N	2	1	3	\N	16	2026-05-31	f	16
15	15	80.00	0.00	0.00	80.00	cash		t	2026-05-31 05:22:32.098284+03	\N	\N	2	1	3	\N	15	2026-05-31	f	15
14	14	80.00	0.00	0.00	80.00	cash		t	2026-05-31 05:21:55.15515+03	\N	\N	2	1	3	\N	14	2026-05-31	f	14
13	13	120.00	0.00	0.00	120.00	cash		t	2026-05-31 05:20:57.485305+03	\N	\N	2	1	1	\N	13	2026-05-31	f	13
12	12	600.00	0.00	0.00	600.00	cash		t	2026-05-31 05:19:10.392543+03	\N	\N	2	1	1	\N	12	2026-05-31	f	12
11	11	100.00	0.00	0.00	100.00	cash		t	2026-05-31 05:18:24.198981+03	\N	\N	2	1	1	\N	11	2026-05-31	f	11
10	10	180.00	0.00	0.00	180.00	cash		t	2026-05-31 05:16:07.986835+03	\N	\N	2	1	1	\N	10	2026-05-31	f	10
9	9	180.00	0.00	0.00	180.00	cash		t	2026-05-31 05:14:22.257121+03	\N	\N	2	1	1	\N	9	2026-05-31	f	9
8	8	180.00	0.00	0.00	180.00	cash		t	2026-05-30 06:37:45.787447+03	\N	\N	2	1	3	\N	8	2026-05-30	f	8
7	7	720.00	0.00	0.00	720.00	cash		t	2026-05-30 06:27:53.992711+03	\N	\N	2	1	3	\N	7	2026-05-30	f	7
6	6	180.00	10.00	0.00	170.00	cash		t	2026-05-30 06:25:40.962823+03	\N	\N	2	1	3	\N	6	2026-05-30	f	6
5	5	600.00	0.00	0.00	600.00	cash		t	2026-05-30 05:37:36.724454+03	\N	\N	2	1	\N	\N	5	2026-05-30	f	5
4	4	80.00	0.00	0.00	80.00	cash		t	2026-05-26 22:40:16.256098+03	\N	\N	2	1	\N	\N	4	2026-05-26	f	4
36	33	100.00	0.00	0.00	100.00	cash		t	2026-06-18 02:23:57.095331+03	\N	\N	2	1	10	\N	33	2026-06-18	t	33
3	3	600.00	0.00	0.00	600.00	cash		t	2026-05-18 14:49:13.692726+03	\N	\N	2	1	\N	\N	3	2026-05-18	f	3
2	2	300.00	0.00	0.00	300.00	cash		t	2026-05-18 12:20:43.280291+03	\N	\N	2	1	2	\N	2	2026-05-18	f	2
1	1	1000.00	0.00	0.00	1000.00	cash		t	2026-05-18 03:37:41.232644+03	\N	\N	2	1	1	\N	1	2026-05-18	f	1
37	34	180.00	0.00	0.00	180.00	cash		t	2026-06-18 02:24:15.067884+03	\N	\N	2	1	11	\N	34	2026-06-18	f	34
39	35	80.00	0.00	0.00	80.00	cash		t	2026-06-18 02:35:33.981247+03	\N	\N	2	1	\N	\N	35	2026-06-18	f	35
40	36	80.00	0.00	0.00	80.00	cash		t	2026-06-18 02:35:38.421607+03	\N	\N	2	1	\N	\N	36	2026-06-18	f	36
41	37	180.00	0.00	0.00	180.00	cash		t	2026-06-18 02:35:43.048892+03	\N	\N	2	1	\N	\N	37	2026-06-18	f	37
42	38	180.00	0.00	0.00	180.00	cash		t	2026-06-18 02:35:51.033254+03	\N	\N	2	1	12	\N	38	2026-06-18	f	38
43	39	180.00	0.00	0.00	180.00	cash		t	2026-06-18 02:36:06.353604+03	\N	\N	2	1	13	\N	39	2026-06-18	f	39
45	41	100.00	0.00	0.00	100.00	cash		t	2026-06-18 02:38:11.089004+03	\N	\N	2	1	14	\N	41	2026-06-18	t	41
44	40	600.00	0.00	0.00	600.00	cash		t	2026-06-18 02:37:11.174722+03	\N	\N	2	1	\N	\N	40	2026-06-18	t	40
46	42	600.00	0.00	0.00	600.00	cash		t	2026-06-18 02:41:33.712136+03	\N	\N	2	1	\N	\N	42	2026-06-18	f	42
48	44	80.00	0.00	0.00	80.00	cash		t	2026-06-18 02:45:05.601983+03	\N	\N	2	1	\N	\N	44	2026-06-18	f	44
49	45	80.00	0.00	0.00	80.00	cash		t	2026-06-18 02:45:19.739137+03	\N	\N	2	1	\N	\N	45	2026-06-18	f	45
50	46	180.00	0.00	0.00	180.00	cash		t	2026-06-18 02:46:22.23191+03	\N	\N	2	1	3	\N	46	2026-06-18	f	46
51	47	180.00	0.00	0.00	180.00	cash		t	2026-06-18 02:47:16.692265+03	\N	\N	2	1	\N	\N	47	2026-06-18	f	47
52	48	180.00	0.00	0.00	180.00	cash		t	2026-06-18 03:05:08.517882+03	\N	\N	2	1	3	8	48	2026-06-18	f	48
47	43	600.00	0.00	0.00	600.00	cash		t	2026-06-18 02:42:00.745056+03	\N	\N	2	1	15	\N	43	2026-06-18	f	43
\.


--
-- Data for Name: salon_invoiceitem; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_invoiceitem (id, quantity, price, total, invoice_id, product_id, service_id) FROM stdin;
1	1	300.00	300.00	1	\N	3
2	1	600.00	600.00	1	\N	5
3	1	100.00	100.00	1	\N	1
4	1	100.00	100.00	2	\N	1
5	1	120.00	120.00	2	\N	2
6	1	80.00	80.00	2	\N	4
7	1	600.00	600.00	3	\N	5
8	1	80.00	80.00	4	\N	4
9	1	600.00	600.00	5	\N	5
10	1	100.00	100.00	6	\N	1
11	1	80.00	80.00	6	\N	4
12	1	600.00	600.00	7	\N	5
13	1	120.00	120.00	7	\N	2
14	1	100.00	100.00	8	\N	1
15	1	80.00	80.00	8	\N	4
16	1	80.00	80.00	9	\N	4
17	1	100.00	100.00	9	\N	1
18	1	100.00	100.00	10	\N	1
19	1	80.00	80.00	10	\N	4
20	1	100.00	100.00	11	\N	1
21	1	600.00	600.00	12	\N	5
22	1	120.00	120.00	13	\N	2
23	1	80.00	80.00	14	\N	4
24	1	80.00	80.00	15	\N	4
25	1	120.00	120.00	16	\N	2
26	1	120.00	120.00	17	\N	2
27	1	120.00	120.00	18	\N	2
28	1	120.00	120.00	19	\N	2
29	1	80.00	80.00	20	\N	4
30	1	100.00	100.00	21	\N	1
31	1	80.00	80.00	22	\N	4
32	1	100.00	100.00	23	\N	1
33	1	100.00	100.00	24	\N	1
34	1	100.00	100.00	25	\N	1
35	1	80.00	80.00	26	\N	4
36	1	100.00	100.00	27	\N	1
37	1	80.00	80.00	28	\N	4
38	1	80.00	80.00	29	\N	4
39	1	100.00	100.00	29	\N	1
40	1	80.00	80.00	30	\N	4
41	1	100.00	100.00	30	\N	1
42	2	80.00	160.00	31	\N	4
43	1	100.00	100.00	32	\N	1
44	1	120.00	120.00	32	\N	2
47	1	80.00	80.00	37	\N	4
48	1	100.00	100.00	37	\N	1
49	1	100.00	100.00	36	\N	1
50	1	80.00	80.00	39	\N	4
51	1	80.00	80.00	40	\N	4
52	1	80.00	80.00	41	\N	4
53	1	100.00	100.00	41	\N	1
54	1	80.00	80.00	42	\N	4
55	1	100.00	100.00	42	\N	1
56	1	80.00	80.00	43	\N	4
57	1	100.00	100.00	43	\N	1
58	1	600.00	600.00	44	\N	5
63	1	100.00	100.00	45	\N	1
66	1	600.00	600.00	46	\N	5
67	1	80.00	80.00	48	\N	4
68	1	80.00	80.00	49	\N	4
69	1	80.00	80.00	50	\N	4
70	1	100.00	100.00	50	\N	1
71	1	80.00	80.00	51	\N	4
72	1	100.00	100.00	51	\N	1
73	1	100.00	100.00	52	\N	1
74	1	80.00	80.00	52	\N	4
75	1	600.00	600.00	47	\N	5
\.


--
-- Data for Name: salon_product; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_product (id, name, code, price, cost, stock, min_stock, is_active, created_at, branch_id, category_id) FROM stdin;
1	sdsd		100.00	20.00	1	2	f	2026-06-17 03:43:19.4874+03	2	\N
3	test	99	20.00	10.00	0	5	t	2026-06-18 03:40:39.734072+03	2	\N
5	يس	100	0.00	0.00	0	5	t	2026-06-18 03:57:27.03975+03	2	\N
2	كريم	1	200.00	100.00	997	5	t	2026-06-18 03:29:52.275228+03	2	\N
\.


--
-- Data for Name: salon_purchaseinvoice; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_purchaseinvoice (id, serial_number, notes, created_at, branch_id, created_by_id) FROM stdin;
3	1		2026-06-18 03:45:40.951518+03	2	1
\.


--
-- Data for Name: salon_purchaseinvoiceitem; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_purchaseinvoiceitem (id, quantity, cost, price, product_id, purchase_id) FROM stdin;
3	1002	100.00	200.00	2	3
\.


--
-- Data for Name: salon_salarypayment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_salarypayment (id, serial_number, amount, month, year, payment_method, notes, created_at, bank_id, branch_id, created_by_id, employee_id, daily_number) FROM stdin;
1	SAL-2-20260617-0001	200.00	6	2026	cash		2026-06-17 03:46:36.574146+03	\N	2	1	1	0
\.


--
-- Data for Name: salon_salonsettings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_salonsettings (id, salon_name, phone, address, currency, invoice_header, invoice_footer, whatsapp_footer, receipt_size, tax_rate, auto_backup, sms_notifications, updated_at, branch_id, logo) FROM stdin;
2	Salon Pro			EGP		شكراً لزيارتكم!	نتمنى لكم يوماً سعيداً 💈\nفي انتظاركم دائماً!	80mm	0.00	f	f	2026-06-17 03:41:34.144962+03	2	
1	TAJ	01029029992	villa 1, Mohamed Abdelwahab st. , plot3, El Sherouk	EGP	jlghfjkgfgjkfgfkfjkh	شكراً لزيارتكم!k.hkljkl	نتمنى لكم يوماً سعيداً 💈\r\nفي انتظاركم دائماً!	80mm	0.00	f	f	2026-06-18 19:40:39.250218+03	\N	salon/logo/TAJ_JEWELRY_logo_in_pure_black_color_on_white_background_high_quality_profess_Zg4GcQc.jpg
\.


--
-- Data for Name: salon_service; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_service (id, name, code, price, cost, duration, is_active, created_at, category_id) FROM stdin;
1	شعر		100.00	100.00	30	t	2026-05-18 03:35:31.689603+03	\N
2	دقن		120.00	120.00	30	t	2026-05-18 03:35:44.313021+03	\N
3	مساج		300.00	300.00	30	t	2026-05-18 03:36:00.511522+03	\N
4	فوطه سخنه		80.00	80.00	30	t	2026-05-18 03:36:23.663559+03	\N
5	بروتين		600.00	600.00	30	t	2026-05-18 03:37:03.724838+03	\N
6	مشمش	1	300.00	0.00	30	f	2026-06-18 04:14:53.703965+03	\N
\.


--
-- Data for Name: salon_stockmovement; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_stockmovement (id, movement_type, quantity, cost, notes, date, created_at, branch_id, created_by_id, product_id, reference_invoice_id, serial_number, daily_number, reference_consumption_id) FROM stdin;
1	out	2	90.00		2026-06-17	2026-06-17 03:43:55.22183+03	2	1	1	\N	1	1	\N
4	in	1002	100.00	مشتريات #1	2026-06-18	2026-06-18 03:45:40.975089+03	2	1	2	3	1	1	\N
5	out	5	100.00	استهلاك #1	2026-06-18	2026-06-18 03:58:16.809941+03	2	1	2	\N	1	1	1
\.


--
-- Data for Name: salon_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone, photo, is_barber, commission_rate, can_pos, can_inventory, can_expenses, can_reports, can_settings, can_users, branch_id, can_audit, can_bookings, can_customers, can_delete_bookings, can_delete_employees, can_delete_expenses, can_delete_inventory, can_delete_pos, can_employees, can_services) FROM stdin;
4	pbkdf2_sha256$1200000$4FwJ80tIiLZyAz2kjA2yz2$dVwX3P8fPoZO8SYri5HchPEi5U2T77Ao5wEbfHH+S7w=	2026-05-30 07:42:14.048043+03	f	mm	mm	mm	mm@gmail.com	f	t	2026-05-30 07:30:11.323463+03			f	0.00	t	f	f	f	f	f	4	f	t	t	f	f	f	f	f	f	t
5	pbkdf2_sha256$1200000$YrpOI7cPh6f6xix6lc8SLZ$TlzwKJuxFaNO7/4M52pSWb1TfVt6jbZJTfVoVv14H/g=	2026-05-30 07:43:30.389289+03	f	kk	kk	kk	mm@gmail.com	f	t	2026-05-30 07:43:06.29427+03			f	0.00	t	t	f	f	f	f	2	f	t	t	f	f	f	f	f	f	t
1	pbkdf2_sha256$1200000$sBLjwz2f4UwuNXB9SWbQC1$Osq0jom3zWOzZaBk8TaSdwQs0g0tqRM90VEEZuJMLJ8=	2026-06-18 03:40:39.769627+03	t	Nayel				t	t	2026-05-18 02:22:29.822211+03			f	0.00	t	t	t	t	f	f	\N	f	t	t	f	f	f	f	f	f	t
\.


--
-- Data for Name: salon_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: salon_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.salon_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 156, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 39, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 35, true);


--
-- Name: employees_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_employee_id_seq', 1, true);


--
-- Name: employees_employeegroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_employeegroup_id_seq', 1, true);


--
-- Name: employees_employeetransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_employeetransaction_id_seq', 1, false);


--
-- Name: employees_payrollbatch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_payrollbatch_id_seq', 1, false);


--
-- Name: employees_payrollline_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_payrollline_id_seq', 1, false);


--
-- Name: employees_rewardpenalty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.employees_rewardpenalty_id_seq', 1, false);


--
-- Name: salon_advancereturn_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_advancereturn_id_seq', 1, false);


--
-- Name: salon_auditlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_auditlog_id_seq', 7, true);


--
-- Name: salon_bank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_bank_id_seq', 1, false);


--
-- Name: salon_booking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_booking_id_seq', 8, true);


--
-- Name: salon_booking_services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_booking_services_id_seq', 3, true);


--
-- Name: salon_branch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_branch_id_seq', 4, true);


--
-- Name: salon_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_category_id_seq', 1, false);


--
-- Name: salon_consumptioninvoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_consumptioninvoice_id_seq', 1, true);


--
-- Name: salon_consumptioninvoiceitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_consumptioninvoiceitem_id_seq', 1, true);


--
-- Name: salon_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_customer_id_seq', 15, true);


--
-- Name: salon_dailyqueuenumber_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_dailyqueuenumber_id_seq', 8, true);


--
-- Name: salon_documentcounter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_documentcounter_id_seq', 6, true);


--
-- Name: salon_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_employee_id_seq', 1, true);


--
-- Name: salon_employeeadvance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_employeeadvance_id_seq', 1, false);


--
-- Name: salon_expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_expense_id_seq', 1, true);


--
-- Name: salon_expensereturn_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_expensereturn_id_seq', 1, false);


--
-- Name: salon_expensetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_expensetype_id_seq', 1, true);


--
-- Name: salon_expensevoucher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_expensevoucher_id_seq', 2, true);


--
-- Name: salon_financialledger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_financialledger_id_seq', 4, true);


--
-- Name: salon_invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_invoice_id_seq', 52, true);


--
-- Name: salon_invoiceitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_invoiceitem_id_seq', 75, true);


--
-- Name: salon_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_product_id_seq', 5, true);


--
-- Name: salon_purchaseinvoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_purchaseinvoice_id_seq', 3, true);


--
-- Name: salon_purchaseinvoiceitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_purchaseinvoiceitem_id_seq', 3, true);


--
-- Name: salon_salarypayment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_salarypayment_id_seq', 1, true);


--
-- Name: salon_salonsettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_salonsettings_id_seq', 2, true);


--
-- Name: salon_service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_service_id_seq', 6, true);


--
-- Name: salon_stockmovement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_stockmovement_id_seq', 5, true);


--
-- Name: salon_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_user_groups_id_seq', 1, false);


--
-- Name: salon_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_user_id_seq', 5, true);


--
-- Name: salon_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.salon_user_user_permissions_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: employees_employee employees_employee_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_code_key UNIQUE (code);


--
-- Name: employees_employee employees_employee_phone_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_phone_key UNIQUE (phone);


--
-- Name: employees_employee employees_employee_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_pkey PRIMARY KEY (id);


--
-- Name: employees_employeegroup employees_employeegroup_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeegroup
    ADD CONSTRAINT employees_employeegroup_code_key UNIQUE (code);


--
-- Name: employees_employeegroup employees_employeegroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeegroup
    ADD CONSTRAINT employees_employeegroup_pkey PRIMARY KEY (id);


--
-- Name: employees_employeetransaction employees_employeetransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetransaction_pkey PRIMARY KEY (id);


--
-- Name: employees_payrollbatch employees_payrollbatch_branch_id_group_id_batch_7de88e61_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbatch_branch_id_group_id_batch_7de88e61_uniq UNIQUE (branch_id, group_id, batch_no);


--
-- Name: employees_payrollbatch employees_payrollbatch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbatch_pkey PRIMARY KEY (id);


--
-- Name: employees_payrollline employees_payrollline_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollline
    ADD CONSTRAINT employees_payrollline_pkey PRIMARY KEY (id);


--
-- Name: employees_rewardpenalty employees_rewardpenalty_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_rewardpenalty
    ADD CONSTRAINT employees_rewardpenalty_pkey PRIMARY KEY (id);


--
-- Name: employees_rewardpenalty employees_rewardpenalty_serial_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_rewardpenalty
    ADD CONSTRAINT employees_rewardpenalty_serial_key UNIQUE (serial);


--
-- Name: salon_advancereturn salon_advancereturn_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_advancereturn
    ADD CONSTRAINT salon_advancereturn_pkey PRIMARY KEY (id);


--
-- Name: salon_auditlog salon_auditlog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_auditlog
    ADD CONSTRAINT salon_auditlog_pkey PRIMARY KEY (id);


--
-- Name: salon_bank salon_bank_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_bank
    ADD CONSTRAINT salon_bank_pkey PRIMARY KEY (id);


--
-- Name: salon_booking salon_booking_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking
    ADD CONSTRAINT salon_booking_pkey PRIMARY KEY (id);


--
-- Name: salon_booking_services salon_booking_services_booking_id_service_id_00b2654b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking_services
    ADD CONSTRAINT salon_booking_services_booking_id_service_id_00b2654b_uniq UNIQUE (booking_id, service_id);


--
-- Name: salon_booking_services salon_booking_services_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking_services
    ADD CONSTRAINT salon_booking_services_pkey PRIMARY KEY (id);


--
-- Name: salon_branch salon_branch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_branch
    ADD CONSTRAINT salon_branch_pkey PRIMARY KEY (id);


--
-- Name: salon_category salon_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_category
    ADD CONSTRAINT salon_category_pkey PRIMARY KEY (id);


--
-- Name: salon_consumptioninvoice salon_consumptioninvoice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoice
    ADD CONSTRAINT salon_consumptioninvoice_pkey PRIMARY KEY (id);


--
-- Name: salon_consumptioninvoiceitem salon_consumptioninvoiceitem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoiceitem
    ADD CONSTRAINT salon_consumptioninvoiceitem_pkey PRIMARY KEY (id);


--
-- Name: salon_customer salon_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_customer
    ADD CONSTRAINT salon_customer_pkey PRIMARY KEY (id);


--
-- Name: salon_dailyqueuenumber salon_dailyqueuenumber_branch_id_date_d6fa7b5b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_dailyqueuenumber
    ADD CONSTRAINT salon_dailyqueuenumber_branch_id_date_d6fa7b5b_uniq UNIQUE (branch_id, date);


--
-- Name: salon_dailyqueuenumber salon_dailyqueuenumber_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_dailyqueuenumber
    ADD CONSTRAINT salon_dailyqueuenumber_pkey PRIMARY KEY (id);


--
-- Name: salon_documentcounter salon_documentcounter_branch_id_screen_code_date_f7dcac7b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_documentcounter
    ADD CONSTRAINT salon_documentcounter_branch_id_screen_code_date_f7dcac7b_uniq UNIQUE (branch_id, screen_code, date);


--
-- Name: salon_documentcounter salon_documentcounter_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_documentcounter
    ADD CONSTRAINT salon_documentcounter_pkey PRIMARY KEY (id);


--
-- Name: salon_employee salon_employee_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employee
    ADD CONSTRAINT salon_employee_pkey PRIMARY KEY (id);


--
-- Name: salon_employee salon_employee_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employee
    ADD CONSTRAINT salon_employee_user_id_key UNIQUE (user_id);


--
-- Name: salon_employeeadvance salon_employeeadvance_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employeeadvance
    ADD CONSTRAINT salon_employeeadvance_pkey PRIMARY KEY (id);


--
-- Name: salon_expense salon_expense_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_pkey PRIMARY KEY (id);


--
-- Name: salon_expense salon_expense_salary_payment_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_salary_payment_id_key UNIQUE (salary_payment_id);


--
-- Name: salon_expensereturn salon_expensereturn_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensereturn
    ADD CONSTRAINT salon_expensereturn_pkey PRIMARY KEY (id);


--
-- Name: salon_expensetype salon_expensetype_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensetype
    ADD CONSTRAINT salon_expensetype_pkey PRIMARY KEY (id);


--
-- Name: salon_expensevoucher salon_expensevoucher_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensevoucher
    ADD CONSTRAINT salon_expensevoucher_pkey PRIMARY KEY (id);


--
-- Name: salon_financialledger salon_financialledger_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_financialledger
    ADD CONSTRAINT salon_financialledger_pkey PRIMARY KEY (id);


--
-- Name: salon_invoice salon_invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_pkey PRIMARY KEY (id);


--
-- Name: salon_invoiceitem salon_invoiceitem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoiceitem
    ADD CONSTRAINT salon_invoiceitem_pkey PRIMARY KEY (id);


--
-- Name: salon_product salon_product_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_product
    ADD CONSTRAINT salon_product_pkey PRIMARY KEY (id);


--
-- Name: salon_purchaseinvoice salon_purchaseinvoice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoice
    ADD CONSTRAINT salon_purchaseinvoice_pkey PRIMARY KEY (id);


--
-- Name: salon_purchaseinvoiceitem salon_purchaseinvoiceitem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoiceitem
    ADD CONSTRAINT salon_purchaseinvoiceitem_pkey PRIMARY KEY (id);


--
-- Name: salon_salarypayment salon_salarypayment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salarypayment
    ADD CONSTRAINT salon_salarypayment_pkey PRIMARY KEY (id);


--
-- Name: salon_salonsettings salon_salonsettings_branch_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salonsettings
    ADD CONSTRAINT salon_salonsettings_branch_id_key UNIQUE (branch_id);


--
-- Name: salon_salonsettings salon_salonsettings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salonsettings
    ADD CONSTRAINT salon_salonsettings_pkey PRIMARY KEY (id);


--
-- Name: salon_service salon_service_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_service
    ADD CONSTRAINT salon_service_pkey PRIMARY KEY (id);


--
-- Name: salon_stockmovement salon_stockmovement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_stockmovement
    ADD CONSTRAINT salon_stockmovement_pkey PRIMARY KEY (id);


--
-- Name: salon_user_groups salon_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_groups
    ADD CONSTRAINT salon_user_groups_pkey PRIMARY KEY (id);


--
-- Name: salon_user_groups salon_user_groups_user_id_group_id_2da4cfaa_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_groups
    ADD CONSTRAINT salon_user_groups_user_id_group_id_2da4cfaa_uniq UNIQUE (user_id, group_id);


--
-- Name: salon_user salon_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user
    ADD CONSTRAINT salon_user_pkey PRIMARY KEY (id);


--
-- Name: salon_user_user_permissions salon_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_user_permissions
    ADD CONSTRAINT salon_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: salon_user_user_permissions salon_user_user_permissions_user_id_permission_id_77565b92_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_user_permissions
    ADD CONSTRAINT salon_user_user_permissions_user_id_permission_id_77565b92_uniq UNIQUE (user_id, permission_id);


--
-- Name: salon_user salon_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user
    ADD CONSTRAINT salon_user_username_key UNIQUE (username);


--
-- Name: salon_consumptioninvoice unique_branch_consumption_serial; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoice
    ADD CONSTRAINT unique_branch_consumption_serial UNIQUE (branch_id, serial_number);


--
-- Name: salon_expensevoucher unique_branch_expense_voucher_serial; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensevoucher
    ADD CONSTRAINT unique_branch_expense_voucher_serial UNIQUE (branch_id, voucher_type, serial_number);


--
-- Name: salon_invoice unique_branch_invoice_serial; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT unique_branch_invoice_serial UNIQUE (branch_id, serial_number);


--
-- Name: salon_purchaseinvoice unique_branch_purchase_serial; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoice
    ADD CONSTRAINT unique_branch_purchase_serial UNIQUE (branch_id, serial_number);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: employees_employee_branch_id_16aa717b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employee_branch_id_16aa717b ON public.employees_employee USING btree (branch_id);


--
-- Name: employees_employee_created_by_id_bfa47e39; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employee_created_by_id_bfa47e39 ON public.employees_employee USING btree (created_by_id);


--
-- Name: employees_employee_group_id_c5587bba; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employee_group_id_c5587bba ON public.employees_employee USING btree (group_id);


--
-- Name: employees_employee_phone_cdfc871b_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employee_phone_cdfc871b_like ON public.employees_employee USING btree (phone varchar_pattern_ops);


--
-- Name: employees_employee_updated_by_id_546c8556; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employee_updated_by_id_546c8556 ON public.employees_employee USING btree (updated_by_id);


--
-- Name: employees_employeegroup_created_by_id_fc92f23d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeegroup_created_by_id_fc92f23d ON public.employees_employeegroup USING btree (created_by_id);


--
-- Name: employees_employeegroup_updated_by_id_835ee28b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeegroup_updated_by_id_835ee28b ON public.employees_employeegroup USING btree (updated_by_id);


--
-- Name: employees_employeetransaction_bank_id_02239859; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeetransaction_bank_id_02239859 ON public.employees_employeetransaction USING btree (bank_id);


--
-- Name: employees_employeetransaction_branch_id_68a6a9cd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeetransaction_branch_id_68a6a9cd ON public.employees_employeetransaction USING btree (branch_id);


--
-- Name: employees_employeetransaction_created_by_id_da6a173c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeetransaction_created_by_id_da6a173c ON public.employees_employeetransaction USING btree (created_by_id);


--
-- Name: employees_employeetransaction_employee_id_37a3e978; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeetransaction_employee_id_37a3e978 ON public.employees_employeetransaction USING btree (employee_id);


--
-- Name: employees_employeetransaction_ledger_entry_id_89e218a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeetransaction_ledger_entry_id_89e218a7 ON public.employees_employeetransaction USING btree (ledger_entry_id);


--
-- Name: employees_employeetransaction_updated_by_id_c6e097ec; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_employeetransaction_updated_by_id_c6e097ec ON public.employees_employeetransaction USING btree (updated_by_id);


--
-- Name: employees_payrollbatch_bank_id_c94e33ae; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollbatch_bank_id_c94e33ae ON public.employees_payrollbatch USING btree (bank_id);


--
-- Name: employees_payrollbatch_branch_id_824ffdfb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollbatch_branch_id_824ffdfb ON public.employees_payrollbatch USING btree (branch_id);


--
-- Name: employees_payrollbatch_created_by_id_589f26da; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollbatch_created_by_id_589f26da ON public.employees_payrollbatch USING btree (created_by_id);


--
-- Name: employees_payrollbatch_group_id_756cfb89; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollbatch_group_id_756cfb89 ON public.employees_payrollbatch USING btree (group_id);


--
-- Name: employees_payrollbatch_ledger_entry_id_9c65139d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollbatch_ledger_entry_id_9c65139d ON public.employees_payrollbatch USING btree (ledger_entry_id);


--
-- Name: employees_payrollbatch_updated_by_id_e5aefed4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollbatch_updated_by_id_e5aefed4 ON public.employees_payrollbatch USING btree (updated_by_id);


--
-- Name: employees_payrollline_batch_id_72f2f128; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollline_batch_id_72f2f128 ON public.employees_payrollline USING btree (batch_id);


--
-- Name: employees_payrollline_created_by_id_45abb33e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollline_created_by_id_45abb33e ON public.employees_payrollline USING btree (created_by_id);


--
-- Name: employees_payrollline_employee_id_d8a4931c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollline_employee_id_d8a4931c ON public.employees_payrollline USING btree (employee_id);


--
-- Name: employees_payrollline_updated_by_id_d372fad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_payrollline_updated_by_id_d372fad4 ON public.employees_payrollline USING btree (updated_by_id);


--
-- Name: employees_rewardpenalty_created_by_id_67837b43; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_rewardpenalty_created_by_id_67837b43 ON public.employees_rewardpenalty USING btree (created_by_id);


--
-- Name: employees_rewardpenalty_employee_id_80d8dc3a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_rewardpenalty_employee_id_80d8dc3a ON public.employees_rewardpenalty USING btree (employee_id);


--
-- Name: employees_rewardpenalty_updated_by_id_5752f4a2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX employees_rewardpenalty_updated_by_id_5752f4a2 ON public.employees_rewardpenalty USING btree (updated_by_id);


--
-- Name: salon_advancereturn_advance_id_e5e34887; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_advancereturn_advance_id_e5e34887 ON public.salon_advancereturn USING btree (advance_id);


--
-- Name: salon_advancereturn_branch_id_caff267b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_advancereturn_branch_id_caff267b ON public.salon_advancereturn USING btree (branch_id);


--
-- Name: salon_advancereturn_created_by_id_e3e7d4b5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_advancereturn_created_by_id_e3e7d4b5 ON public.salon_advancereturn USING btree (created_by_id);


--
-- Name: salon_auditlog_branch_id_7f2ca72f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_auditlog_branch_id_7f2ca72f ON public.salon_auditlog USING btree (branch_id);


--
-- Name: salon_auditlog_user_id_8164f1a3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_auditlog_user_id_8164f1a3 ON public.salon_auditlog USING btree (user_id);


--
-- Name: salon_bank_branch_id_bb0b927c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_bank_branch_id_bb0b927c ON public.salon_bank USING btree (branch_id);


--
-- Name: salon_booking_barber_id_ccf3b0b9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_booking_barber_id_ccf3b0b9 ON public.salon_booking USING btree (barber_id);


--
-- Name: salon_booking_branch_id_160fe177; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_booking_branch_id_160fe177 ON public.salon_booking USING btree (branch_id);


--
-- Name: salon_booking_services_booking_id_057e3f36; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_booking_services_booking_id_057e3f36 ON public.salon_booking_services USING btree (booking_id);


--
-- Name: salon_booking_services_service_id_2a25587b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_booking_services_service_id_2a25587b ON public.salon_booking_services USING btree (service_id);


--
-- Name: salon_consumptioninvoice_branch_id_415a54df; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_consumptioninvoice_branch_id_415a54df ON public.salon_consumptioninvoice USING btree (branch_id);


--
-- Name: salon_consumptioninvoice_created_by_id_ad81fe2a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_consumptioninvoice_created_by_id_ad81fe2a ON public.salon_consumptioninvoice USING btree (created_by_id);


--
-- Name: salon_consumptioninvoiceitem_consumption_id_fe35927a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_consumptioninvoiceitem_consumption_id_fe35927a ON public.salon_consumptioninvoiceitem USING btree (consumption_id);


--
-- Name: salon_consumptioninvoiceitem_product_id_906ffb53; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_consumptioninvoiceitem_product_id_906ffb53 ON public.salon_consumptioninvoiceitem USING btree (product_id);


--
-- Name: salon_customer_branch_id_31e29fd8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_customer_branch_id_31e29fd8 ON public.salon_customer USING btree (branch_id);


--
-- Name: salon_dailyqueuenumber_branch_id_ffb4a075; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_dailyqueuenumber_branch_id_ffb4a075 ON public.salon_dailyqueuenumber USING btree (branch_id);


--
-- Name: salon_documentcounter_branch_id_1a4031d7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_documentcounter_branch_id_1a4031d7 ON public.salon_documentcounter USING btree (branch_id);


--
-- Name: salon_employee_branch_id_7437cae7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_employee_branch_id_7437cae7 ON public.salon_employee USING btree (branch_id);


--
-- Name: salon_employeeadvance_branch_id_51406523; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_employeeadvance_branch_id_51406523 ON public.salon_employeeadvance USING btree (branch_id);


--
-- Name: salon_employeeadvance_created_by_id_5838ec1e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_employeeadvance_created_by_id_5838ec1e ON public.salon_employeeadvance USING btree (created_by_id);


--
-- Name: salon_employeeadvance_deducted_in_id_e54a65cc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_employeeadvance_deducted_in_id_e54a65cc ON public.salon_employeeadvance USING btree (deducted_in_id);


--
-- Name: salon_employeeadvance_employee_id_b152d06e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_employeeadvance_employee_id_b152d06e ON public.salon_employeeadvance USING btree (employee_id);


--
-- Name: salon_expense_bank_id_8594a1c2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expense_bank_id_8594a1c2 ON public.salon_expense USING btree (bank_id);


--
-- Name: salon_expense_branch_id_098eee01; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expense_branch_id_098eee01 ON public.salon_expense USING btree (branch_id);


--
-- Name: salon_expense_category_id_65c4dbfd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expense_category_id_65c4dbfd ON public.salon_expense USING btree (category_id);


--
-- Name: salon_expense_created_by_id_551ba982; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expense_created_by_id_551ba982 ON public.salon_expense USING btree (created_by_id);


--
-- Name: salon_expensereturn_bank_id_4a262084; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensereturn_bank_id_4a262084 ON public.salon_expensereturn USING btree (bank_id);


--
-- Name: salon_expensereturn_branch_id_53b66006; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensereturn_branch_id_53b66006 ON public.salon_expensereturn USING btree (branch_id);


--
-- Name: salon_expensereturn_created_by_id_00eb4aba; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensereturn_created_by_id_00eb4aba ON public.salon_expensereturn USING btree (created_by_id);


--
-- Name: salon_expensereturn_expense_id_1d1821e9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensereturn_expense_id_1d1821e9 ON public.salon_expensereturn USING btree (expense_id);


--
-- Name: salon_expensetype_branch_id_48151b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensetype_branch_id_48151b1c ON public.salon_expensetype USING btree (branch_id);


--
-- Name: salon_expensevoucher_bank_id_e66b30dc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensevoucher_bank_id_e66b30dc ON public.salon_expensevoucher USING btree (bank_id);


--
-- Name: salon_expensevoucher_branch_id_c68d0249; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensevoucher_branch_id_c68d0249 ON public.salon_expensevoucher USING btree (branch_id);


--
-- Name: salon_expensevoucher_created_by_id_3533d17c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensevoucher_created_by_id_3533d17c ON public.salon_expensevoucher USING btree (created_by_id);


--
-- Name: salon_expensevoucher_expense_type_id_af93f514; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_expensevoucher_expense_type_id_af93f514 ON public.salon_expensevoucher USING btree (expense_type_id);


--
-- Name: salon_financialledger_bank_id_e9399aeb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_financialledger_bank_id_e9399aeb ON public.salon_financialledger USING btree (bank_id);


--
-- Name: salon_financialledger_branch_id_7408aafc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_financialledger_branch_id_7408aafc ON public.salon_financialledger USING btree (branch_id);


--
-- Name: salon_financialledger_created_by_id_f10ff774; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_financialledger_created_by_id_f10ff774 ON public.salon_financialledger USING btree (created_by_id);


--
-- Name: salon_invoice_bank_id_1555431b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoice_bank_id_1555431b ON public.salon_invoice USING btree (bank_id);


--
-- Name: salon_invoice_barber_id_1bd1ab65; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoice_barber_id_1bd1ab65 ON public.salon_invoice USING btree (barber_id);


--
-- Name: salon_invoice_booking_id_cd1bbc2e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoice_booking_id_cd1bbc2e ON public.salon_invoice USING btree (booking_id);


--
-- Name: salon_invoice_branch_id_af606db1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoice_branch_id_af606db1 ON public.salon_invoice USING btree (branch_id);


--
-- Name: salon_invoice_created_by_id_96e7d717; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoice_created_by_id_96e7d717 ON public.salon_invoice USING btree (created_by_id);


--
-- Name: salon_invoice_customer_id_36323656; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoice_customer_id_36323656 ON public.salon_invoice USING btree (customer_id);


--
-- Name: salon_invoiceitem_invoice_id_55d43681; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoiceitem_invoice_id_55d43681 ON public.salon_invoiceitem USING btree (invoice_id);


--
-- Name: salon_invoiceitem_product_id_79fd85f4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoiceitem_product_id_79fd85f4 ON public.salon_invoiceitem USING btree (product_id);


--
-- Name: salon_invoiceitem_service_id_9066907a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_invoiceitem_service_id_9066907a ON public.salon_invoiceitem USING btree (service_id);


--
-- Name: salon_product_branch_id_fdd06562; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_product_branch_id_fdd06562 ON public.salon_product USING btree (branch_id);


--
-- Name: salon_product_category_id_ac41de83; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_product_category_id_ac41de83 ON public.salon_product USING btree (category_id);


--
-- Name: salon_purchaseinvoice_branch_id_5450c4b5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_purchaseinvoice_branch_id_5450c4b5 ON public.salon_purchaseinvoice USING btree (branch_id);


--
-- Name: salon_purchaseinvoice_created_by_id_3fa0c4dc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_purchaseinvoice_created_by_id_3fa0c4dc ON public.salon_purchaseinvoice USING btree (created_by_id);


--
-- Name: salon_purchaseinvoiceitem_product_id_13c22bd7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_purchaseinvoiceitem_product_id_13c22bd7 ON public.salon_purchaseinvoiceitem USING btree (product_id);


--
-- Name: salon_purchaseinvoiceitem_purchase_id_07aadb38; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_purchaseinvoiceitem_purchase_id_07aadb38 ON public.salon_purchaseinvoiceitem USING btree (purchase_id);


--
-- Name: salon_salarypayment_bank_id_fc228f9f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_salarypayment_bank_id_fc228f9f ON public.salon_salarypayment USING btree (bank_id);


--
-- Name: salon_salarypayment_branch_id_b7b115a2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_salarypayment_branch_id_b7b115a2 ON public.salon_salarypayment USING btree (branch_id);


--
-- Name: salon_salarypayment_created_by_id_30e722e8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_salarypayment_created_by_id_30e722e8 ON public.salon_salarypayment USING btree (created_by_id);


--
-- Name: salon_salarypayment_employee_id_6029a968; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_salarypayment_employee_id_6029a968 ON public.salon_salarypayment USING btree (employee_id);


--
-- Name: salon_service_category_id_0a191ae7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_service_category_id_0a191ae7 ON public.salon_service USING btree (category_id);


--
-- Name: salon_stockmovement_branch_id_f4cd3c25; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_stockmovement_branch_id_f4cd3c25 ON public.salon_stockmovement USING btree (branch_id);


--
-- Name: salon_stockmovement_created_by_id_43cfe1db; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_stockmovement_created_by_id_43cfe1db ON public.salon_stockmovement USING btree (created_by_id);


--
-- Name: salon_stockmovement_product_id_d750188e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_stockmovement_product_id_d750188e ON public.salon_stockmovement USING btree (product_id);


--
-- Name: salon_stockmovement_reference_consumption_id_819c2b57; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_stockmovement_reference_consumption_id_819c2b57 ON public.salon_stockmovement USING btree (reference_consumption_id);


--
-- Name: salon_stockmovement_reference_invoice_id_68ee283c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_stockmovement_reference_invoice_id_68ee283c ON public.salon_stockmovement USING btree (reference_invoice_id);


--
-- Name: salon_user_branch_id_3f9bdf84; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_user_branch_id_3f9bdf84 ON public.salon_user USING btree (branch_id);


--
-- Name: salon_user_groups_group_id_fe6da36e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_user_groups_group_id_fe6da36e ON public.salon_user_groups USING btree (group_id);


--
-- Name: salon_user_groups_user_id_094b69f5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_user_groups_user_id_094b69f5 ON public.salon_user_groups USING btree (user_id);


--
-- Name: salon_user_user_permissions_permission_id_c90b485d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_user_user_permissions_permission_id_c90b485d ON public.salon_user_user_permissions USING btree (permission_id);


--
-- Name: salon_user_user_permissions_user_id_9b6d5e12; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_user_user_permissions_user_id_9b6d5e12 ON public.salon_user_user_permissions USING btree (user_id);


--
-- Name: salon_user_username_c7ad3cec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX salon_user_username_c7ad3cec_like ON public.salon_user USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_salon_user_id FOREIGN KEY (user_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employee employees_employee_branch_id_16aa717b_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_branch_id_16aa717b_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employee employees_employee_created_by_id_bfa47e39_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_created_by_id_bfa47e39_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employee employees_employee_group_id_c5587bba_fk_employees; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_group_id_c5587bba_fk_employees FOREIGN KEY (group_id) REFERENCES public.employees_employeegroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employee employees_employee_updated_by_id_546c8556_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employee
    ADD CONSTRAINT employees_employee_updated_by_id_546c8556_fk_salon_user_id FOREIGN KEY (updated_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeegroup employees_employeegroup_created_by_id_fc92f23d_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeegroup
    ADD CONSTRAINT employees_employeegroup_created_by_id_fc92f23d_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeegroup employees_employeegroup_updated_by_id_835ee28b_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeegroup
    ADD CONSTRAINT employees_employeegroup_updated_by_id_835ee28b_fk_salon_user_id FOREIGN KEY (updated_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeetransaction employees_employeetr_branch_id_68a6a9cd_fk_salon_bra; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetr_branch_id_68a6a9cd_fk_salon_bra FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeetransaction employees_employeetr_created_by_id_da6a173c_fk_salon_use; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetr_created_by_id_da6a173c_fk_salon_use FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeetransaction employees_employeetr_employee_id_37a3e978_fk_employees; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetr_employee_id_37a3e978_fk_employees FOREIGN KEY (employee_id) REFERENCES public.employees_employee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeetransaction employees_employeetr_ledger_entry_id_89e218a7_fk_salon_fin; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetr_ledger_entry_id_89e218a7_fk_salon_fin FOREIGN KEY (ledger_entry_id) REFERENCES public.salon_financialledger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeetransaction employees_employeetr_updated_by_id_c6e097ec_fk_salon_use; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetr_updated_by_id_c6e097ec_fk_salon_use FOREIGN KEY (updated_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_employeetransaction employees_employeetransaction_bank_id_02239859_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_employeetransaction
    ADD CONSTRAINT employees_employeetransaction_bank_id_02239859_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollbatch employees_payrollbat_group_id_756cfb89_fk_employees; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbat_group_id_756cfb89_fk_employees FOREIGN KEY (group_id) REFERENCES public.employees_employeegroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollbatch employees_payrollbat_ledger_entry_id_9c65139d_fk_salon_fin; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbat_ledger_entry_id_9c65139d_fk_salon_fin FOREIGN KEY (ledger_entry_id) REFERENCES public.salon_financialledger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollbatch employees_payrollbatch_bank_id_c94e33ae_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbatch_bank_id_c94e33ae_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollbatch employees_payrollbatch_branch_id_824ffdfb_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbatch_branch_id_824ffdfb_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollbatch employees_payrollbatch_created_by_id_589f26da_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbatch_created_by_id_589f26da_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollbatch employees_payrollbatch_updated_by_id_e5aefed4_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollbatch
    ADD CONSTRAINT employees_payrollbatch_updated_by_id_e5aefed4_fk_salon_user_id FOREIGN KEY (updated_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollline employees_payrolllin_batch_id_72f2f128_fk_employees; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollline
    ADD CONSTRAINT employees_payrolllin_batch_id_72f2f128_fk_employees FOREIGN KEY (batch_id) REFERENCES public.employees_payrollbatch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollline employees_payrolllin_employee_id_d8a4931c_fk_employees; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollline
    ADD CONSTRAINT employees_payrolllin_employee_id_d8a4931c_fk_employees FOREIGN KEY (employee_id) REFERENCES public.employees_employee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollline employees_payrollline_created_by_id_45abb33e_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollline
    ADD CONSTRAINT employees_payrollline_created_by_id_45abb33e_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_payrollline employees_payrollline_updated_by_id_d372fad4_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_payrollline
    ADD CONSTRAINT employees_payrollline_updated_by_id_d372fad4_fk_salon_user_id FOREIGN KEY (updated_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_rewardpenalty employees_rewardpena_employee_id_80d8dc3a_fk_employees; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_rewardpenalty
    ADD CONSTRAINT employees_rewardpena_employee_id_80d8dc3a_fk_employees FOREIGN KEY (employee_id) REFERENCES public.employees_employee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_rewardpenalty employees_rewardpenalty_created_by_id_67837b43_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_rewardpenalty
    ADD CONSTRAINT employees_rewardpenalty_created_by_id_67837b43_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: employees_rewardpenalty employees_rewardpenalty_updated_by_id_5752f4a2_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees_rewardpenalty
    ADD CONSTRAINT employees_rewardpenalty_updated_by_id_5752f4a2_fk_salon_user_id FOREIGN KEY (updated_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_advancereturn salon_advancereturn_advance_id_e5e34887_fk_salon_emp; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_advancereturn
    ADD CONSTRAINT salon_advancereturn_advance_id_e5e34887_fk_salon_emp FOREIGN KEY (advance_id) REFERENCES public.salon_employeeadvance(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_advancereturn salon_advancereturn_branch_id_caff267b_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_advancereturn
    ADD CONSTRAINT salon_advancereturn_branch_id_caff267b_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_advancereturn salon_advancereturn_created_by_id_e3e7d4b5_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_advancereturn
    ADD CONSTRAINT salon_advancereturn_created_by_id_e3e7d4b5_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_auditlog salon_auditlog_branch_id_7f2ca72f_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_auditlog
    ADD CONSTRAINT salon_auditlog_branch_id_7f2ca72f_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_auditlog salon_auditlog_user_id_8164f1a3_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_auditlog
    ADD CONSTRAINT salon_auditlog_user_id_8164f1a3_fk_salon_user_id FOREIGN KEY (user_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_bank salon_bank_branch_id_bb0b927c_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_bank
    ADD CONSTRAINT salon_bank_branch_id_bb0b927c_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_booking salon_booking_barber_id_ccf3b0b9_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking
    ADD CONSTRAINT salon_booking_barber_id_ccf3b0b9_fk_salon_user_id FOREIGN KEY (barber_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_booking salon_booking_branch_id_160fe177_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking
    ADD CONSTRAINT salon_booking_branch_id_160fe177_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_booking_services salon_booking_services_booking_id_057e3f36_fk_salon_booking_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking_services
    ADD CONSTRAINT salon_booking_services_booking_id_057e3f36_fk_salon_booking_id FOREIGN KEY (booking_id) REFERENCES public.salon_booking(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_booking_services salon_booking_services_service_id_2a25587b_fk_salon_service_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_booking_services
    ADD CONSTRAINT salon_booking_services_service_id_2a25587b_fk_salon_service_id FOREIGN KEY (service_id) REFERENCES public.salon_service(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_consumptioninvoiceitem salon_consumptioninv_consumption_id_fe35927a_fk_salon_con; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoiceitem
    ADD CONSTRAINT salon_consumptioninv_consumption_id_fe35927a_fk_salon_con FOREIGN KEY (consumption_id) REFERENCES public.salon_consumptioninvoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_consumptioninvoice salon_consumptioninv_created_by_id_ad81fe2a_fk_salon_use; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoice
    ADD CONSTRAINT salon_consumptioninv_created_by_id_ad81fe2a_fk_salon_use FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_consumptioninvoiceitem salon_consumptioninv_product_id_906ffb53_fk_salon_pro; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoiceitem
    ADD CONSTRAINT salon_consumptioninv_product_id_906ffb53_fk_salon_pro FOREIGN KEY (product_id) REFERENCES public.salon_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_consumptioninvoice salon_consumptioninvoice_branch_id_415a54df_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_consumptioninvoice
    ADD CONSTRAINT salon_consumptioninvoice_branch_id_415a54df_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_customer salon_customer_branch_id_31e29fd8_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_customer
    ADD CONSTRAINT salon_customer_branch_id_31e29fd8_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_dailyqueuenumber salon_dailyqueuenumber_branch_id_ffb4a075_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_dailyqueuenumber
    ADD CONSTRAINT salon_dailyqueuenumber_branch_id_ffb4a075_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_documentcounter salon_documentcounter_branch_id_1a4031d7_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_documentcounter
    ADD CONSTRAINT salon_documentcounter_branch_id_1a4031d7_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_employee salon_employee_branch_id_7437cae7_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employee
    ADD CONSTRAINT salon_employee_branch_id_7437cae7_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_employee salon_employee_user_id_166684b7_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employee
    ADD CONSTRAINT salon_employee_user_id_166684b7_fk_salon_user_id FOREIGN KEY (user_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_employeeadvance salon_employeeadvanc_deducted_in_id_e54a65cc_fk_salon_sal; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employeeadvance
    ADD CONSTRAINT salon_employeeadvanc_deducted_in_id_e54a65cc_fk_salon_sal FOREIGN KEY (deducted_in_id) REFERENCES public.salon_salarypayment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_employeeadvance salon_employeeadvance_branch_id_51406523_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employeeadvance
    ADD CONSTRAINT salon_employeeadvance_branch_id_51406523_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_employeeadvance salon_employeeadvance_created_by_id_5838ec1e_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employeeadvance
    ADD CONSTRAINT salon_employeeadvance_created_by_id_5838ec1e_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_employeeadvance salon_employeeadvance_employee_id_b152d06e_fk_salon_employee_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_employeeadvance
    ADD CONSTRAINT salon_employeeadvance_employee_id_b152d06e_fk_salon_employee_id FOREIGN KEY (employee_id) REFERENCES public.salon_employee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expense salon_expense_bank_id_8594a1c2_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_bank_id_8594a1c2_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expense salon_expense_branch_id_098eee01_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_branch_id_098eee01_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expense salon_expense_category_id_65c4dbfd_fk_salon_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_category_id_65c4dbfd_fk_salon_category_id FOREIGN KEY (category_id) REFERENCES public.salon_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expense salon_expense_created_by_id_551ba982_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_created_by_id_551ba982_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expense salon_expense_salary_payment_id_a7c0e376_fk_salon_sal; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expense
    ADD CONSTRAINT salon_expense_salary_payment_id_a7c0e376_fk_salon_sal FOREIGN KEY (salary_payment_id) REFERENCES public.salon_salarypayment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensereturn salon_expensereturn_bank_id_4a262084_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensereturn
    ADD CONSTRAINT salon_expensereturn_bank_id_4a262084_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensereturn salon_expensereturn_branch_id_53b66006_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensereturn
    ADD CONSTRAINT salon_expensereturn_branch_id_53b66006_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensereturn salon_expensereturn_created_by_id_00eb4aba_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensereturn
    ADD CONSTRAINT salon_expensereturn_created_by_id_00eb4aba_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensereturn salon_expensereturn_expense_id_1d1821e9_fk_salon_expense_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensereturn
    ADD CONSTRAINT salon_expensereturn_expense_id_1d1821e9_fk_salon_expense_id FOREIGN KEY (expense_id) REFERENCES public.salon_expense(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensetype salon_expensetype_branch_id_48151b1c_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensetype
    ADD CONSTRAINT salon_expensetype_branch_id_48151b1c_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensevoucher salon_expensevoucher_bank_id_e66b30dc_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensevoucher
    ADD CONSTRAINT salon_expensevoucher_bank_id_e66b30dc_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensevoucher salon_expensevoucher_branch_id_c68d0249_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensevoucher
    ADD CONSTRAINT salon_expensevoucher_branch_id_c68d0249_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensevoucher salon_expensevoucher_created_by_id_3533d17c_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensevoucher
    ADD CONSTRAINT salon_expensevoucher_created_by_id_3533d17c_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_expensevoucher salon_expensevoucher_expense_type_id_af93f514_fk_salon_exp; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_expensevoucher
    ADD CONSTRAINT salon_expensevoucher_expense_type_id_af93f514_fk_salon_exp FOREIGN KEY (expense_type_id) REFERENCES public.salon_expensetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_financialledger salon_financialledger_bank_id_e9399aeb_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_financialledger
    ADD CONSTRAINT salon_financialledger_bank_id_e9399aeb_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_financialledger salon_financialledger_branch_id_7408aafc_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_financialledger
    ADD CONSTRAINT salon_financialledger_branch_id_7408aafc_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_financialledger salon_financialledger_created_by_id_f10ff774_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_financialledger
    ADD CONSTRAINT salon_financialledger_created_by_id_f10ff774_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoice salon_invoice_bank_id_1555431b_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_bank_id_1555431b_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoice salon_invoice_barber_id_1bd1ab65_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_barber_id_1bd1ab65_fk_salon_user_id FOREIGN KEY (barber_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoice salon_invoice_booking_id_cd1bbc2e_fk_salon_booking_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_booking_id_cd1bbc2e_fk_salon_booking_id FOREIGN KEY (booking_id) REFERENCES public.salon_booking(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoice salon_invoice_branch_id_af606db1_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_branch_id_af606db1_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoice salon_invoice_created_by_id_96e7d717_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_created_by_id_96e7d717_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoice salon_invoice_customer_id_36323656_fk_salon_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoice
    ADD CONSTRAINT salon_invoice_customer_id_36323656_fk_salon_customer_id FOREIGN KEY (customer_id) REFERENCES public.salon_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoiceitem salon_invoiceitem_invoice_id_55d43681_fk_salon_invoice_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoiceitem
    ADD CONSTRAINT salon_invoiceitem_invoice_id_55d43681_fk_salon_invoice_id FOREIGN KEY (invoice_id) REFERENCES public.salon_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoiceitem salon_invoiceitem_product_id_79fd85f4_fk_salon_product_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoiceitem
    ADD CONSTRAINT salon_invoiceitem_product_id_79fd85f4_fk_salon_product_id FOREIGN KEY (product_id) REFERENCES public.salon_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_invoiceitem salon_invoiceitem_service_id_9066907a_fk_salon_service_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_invoiceitem
    ADD CONSTRAINT salon_invoiceitem_service_id_9066907a_fk_salon_service_id FOREIGN KEY (service_id) REFERENCES public.salon_service(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_product salon_product_branch_id_fdd06562_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_product
    ADD CONSTRAINT salon_product_branch_id_fdd06562_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_product salon_product_category_id_ac41de83_fk_salon_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_product
    ADD CONSTRAINT salon_product_category_id_ac41de83_fk_salon_category_id FOREIGN KEY (category_id) REFERENCES public.salon_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_purchaseinvoiceitem salon_purchaseinvoic_product_id_13c22bd7_fk_salon_pro; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoiceitem
    ADD CONSTRAINT salon_purchaseinvoic_product_id_13c22bd7_fk_salon_pro FOREIGN KEY (product_id) REFERENCES public.salon_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_purchaseinvoiceitem salon_purchaseinvoic_purchase_id_07aadb38_fk_salon_pur; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoiceitem
    ADD CONSTRAINT salon_purchaseinvoic_purchase_id_07aadb38_fk_salon_pur FOREIGN KEY (purchase_id) REFERENCES public.salon_purchaseinvoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_purchaseinvoice salon_purchaseinvoice_branch_id_5450c4b5_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoice
    ADD CONSTRAINT salon_purchaseinvoice_branch_id_5450c4b5_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_purchaseinvoice salon_purchaseinvoice_created_by_id_3fa0c4dc_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_purchaseinvoice
    ADD CONSTRAINT salon_purchaseinvoice_created_by_id_3fa0c4dc_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_salarypayment salon_salarypayment_bank_id_fc228f9f_fk_salon_bank_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salarypayment
    ADD CONSTRAINT salon_salarypayment_bank_id_fc228f9f_fk_salon_bank_id FOREIGN KEY (bank_id) REFERENCES public.salon_bank(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_salarypayment salon_salarypayment_branch_id_b7b115a2_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salarypayment
    ADD CONSTRAINT salon_salarypayment_branch_id_b7b115a2_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_salarypayment salon_salarypayment_created_by_id_30e722e8_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salarypayment
    ADD CONSTRAINT salon_salarypayment_created_by_id_30e722e8_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_salarypayment salon_salarypayment_employee_id_6029a968_fk_salon_employee_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salarypayment
    ADD CONSTRAINT salon_salarypayment_employee_id_6029a968_fk_salon_employee_id FOREIGN KEY (employee_id) REFERENCES public.salon_employee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_salonsettings salon_salonsettings_branch_id_9bd80141_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_salonsettings
    ADD CONSTRAINT salon_salonsettings_branch_id_9bd80141_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_service salon_service_category_id_0a191ae7_fk_salon_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_service
    ADD CONSTRAINT salon_service_category_id_0a191ae7_fk_salon_category_id FOREIGN KEY (category_id) REFERENCES public.salon_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_stockmovement salon_stockmovement_branch_id_f4cd3c25_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_stockmovement
    ADD CONSTRAINT salon_stockmovement_branch_id_f4cd3c25_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_stockmovement salon_stockmovement_created_by_id_43cfe1db_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_stockmovement
    ADD CONSTRAINT salon_stockmovement_created_by_id_43cfe1db_fk_salon_user_id FOREIGN KEY (created_by_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_stockmovement salon_stockmovement_product_id_d750188e_fk_salon_product_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_stockmovement
    ADD CONSTRAINT salon_stockmovement_product_id_d750188e_fk_salon_product_id FOREIGN KEY (product_id) REFERENCES public.salon_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_stockmovement salon_stockmovement_reference_consumptio_819c2b57_fk_salon_con; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_stockmovement
    ADD CONSTRAINT salon_stockmovement_reference_consumptio_819c2b57_fk_salon_con FOREIGN KEY (reference_consumption_id) REFERENCES public.salon_consumptioninvoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_stockmovement salon_stockmovement_reference_invoice_id_68ee283c_fk_salon_inv; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_stockmovement
    ADD CONSTRAINT salon_stockmovement_reference_invoice_id_68ee283c_fk_salon_inv FOREIGN KEY (reference_invoice_id) REFERENCES public.salon_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_user salon_user_branch_id_3f9bdf84_fk_salon_branch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user
    ADD CONSTRAINT salon_user_branch_id_3f9bdf84_fk_salon_branch_id FOREIGN KEY (branch_id) REFERENCES public.salon_branch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_user_groups salon_user_groups_group_id_fe6da36e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_groups
    ADD CONSTRAINT salon_user_groups_group_id_fe6da36e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_user_groups salon_user_groups_user_id_094b69f5_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_groups
    ADD CONSTRAINT salon_user_groups_user_id_094b69f5_fk_salon_user_id FOREIGN KEY (user_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_user_user_permissions salon_user_user_perm_permission_id_c90b485d_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_user_permissions
    ADD CONSTRAINT salon_user_user_perm_permission_id_c90b485d_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: salon_user_user_permissions salon_user_user_permissions_user_id_9b6d5e12_fk_salon_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.salon_user_user_permissions
    ADD CONSTRAINT salon_user_user_permissions_user_id_9b6d5e12_fk_salon_user_id FOREIGN KEY (user_id) REFERENCES public.salon_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict yraog5QOpTJf270hka7dccMGMXHH0xmhR1UEdglQPpZCATJ2KbtbKUntzCcMq0x

