from graphviz import Digraph

# Создаем объект графа
diagram = Digraph("company_architecture", format="png")
diagram.attr(rankdir="TB", size="8,5")

# Узлы для информационной архитектуры
diagram.attr("node", shape="ellipse", style="filled", color="lightblue")
diagram.node("data_center", "Централизованное хранилище данных")
diagram.node("integration_bus", "Интеграционная шина данных")
diagram.node("customer_data", "Данные о клиентах")
diagram.node("project_data", "Проектные данные")
diagram.node("finance_data", "Финансовые данные")
diagram.node("employee_data", "Данные сотрудников")

# Связи в информационной архитектуре
diagram.edge("data_center", "customer_data")
diagram.edge("data_center", "project_data")
diagram.edge("data_center", "finance_data")
diagram.edge("data_center", "employee_data")

# Узлы для прикладной архитектуры
diagram.attr("node", shape="box", style="filled", color="lightgreen")
diagram.node("erp_system", "ERP-система (1С)")
diagram.node("crm_system", "CRM-система")
diagram.node("support_portal", "Портал техподдержки")
diagram.node("project_mgmt", "Система управления проектами")
diagram.node("bi_system", "BI-система")

# Связи между информационной и прикладной архитектурами
diagram.edge("customer_data", "crm_system")
diagram.edge("project_data", "project_mgmt")
diagram.edge("finance_data", "erp_system")
diagram.edge("data_center", "bi_system")
diagram.edge("integration_bus", "crm_system")
diagram.edge("integration_bus", "erp_system")
diagram.edge("integration_bus", "bi_system")
diagram.edge("integration_bus", "support_portal")
diagram.edge("integration_bus", "project_mgmt")

# Связи между прикладными компонентами
diagram.edge("crm_system", "support_portal")
diagram.edge("crm_system", "project_mgmt")
diagram.edge("erp_system", "bi_system")
diagram.edge("erp_system", "crm_system")

# Узлы для технической архитектуры
diagram.attr("node", shape="box3d", style="filled", color="lightcoral")
diagram.node("servers", "Серверная инфраструктура")
diagram.node("database", "СУБД")
diagram.node("security", "Системы безопасности (VPN, антивирусы)")
diagram.node("network", "Сетевая инфраструктура")
diagram.node("email_service", "Сервис электронной почты")

# Связи между прикладной и технической архитектурой
diagram.edge("erp_system", "database")
diagram.edge("crm_system", "database")
diagram.edge("project_mgmt", "database")
diagram.edge("bi_system", "database")
diagram.edge("support_portal", "servers")
diagram.edge("integration_bus", "servers")

# Связи между техническими компонентами
diagram.edge("servers", "network")
diagram.edge("network", "security")
diagram.edge("security", "email_service")

# Визуализация диаграммы
diagram.render("company_architecture")
