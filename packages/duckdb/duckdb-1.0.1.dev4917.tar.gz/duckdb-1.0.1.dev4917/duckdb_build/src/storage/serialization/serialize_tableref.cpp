//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_serialization.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#include "duckdb/common/serializer/serializer.hpp"
#include "duckdb/common/serializer/deserializer.hpp"
#include "duckdb/parser/tableref/list.hpp"

namespace duckdb {

void TableRef::Serialize(Serializer &serializer) const {
	serializer.WriteProperty<TableReferenceType>(100, "type", type);
	serializer.WritePropertyWithDefault<string>(101, "alias", alias);
	serializer.WritePropertyWithDefault<unique_ptr<SampleOptions>>(102, "sample", sample);
	serializer.WritePropertyWithDefault<optional_idx>(103, "query_location", query_location, optional_idx());
}

unique_ptr<TableRef> TableRef::Deserialize(Deserializer &deserializer) {
	auto type = deserializer.ReadProperty<TableReferenceType>(100, "type");
	auto alias = deserializer.ReadPropertyWithDefault<string>(101, "alias");
	auto sample = deserializer.ReadPropertyWithDefault<unique_ptr<SampleOptions>>(102, "sample");
	auto query_location = deserializer.ReadPropertyWithExplicitDefault<optional_idx>(103, "query_location", optional_idx());
	unique_ptr<TableRef> result;
	switch (type) {
	case TableReferenceType::BASE_TABLE:
		result = BaseTableRef::Deserialize(deserializer);
		break;
	case TableReferenceType::COLUMN_DATA:
		result = ColumnDataRef::Deserialize(deserializer);
		break;
	case TableReferenceType::EMPTY_FROM:
		result = EmptyTableRef::Deserialize(deserializer);
		break;
	case TableReferenceType::EXPRESSION_LIST:
		result = ExpressionListRef::Deserialize(deserializer);
		break;
	case TableReferenceType::JOIN:
		result = JoinRef::Deserialize(deserializer);
		break;
	case TableReferenceType::PIVOT:
		result = PivotRef::Deserialize(deserializer);
		break;
	case TableReferenceType::SHOW_REF:
		result = ShowRef::Deserialize(deserializer);
		break;
	case TableReferenceType::SUBQUERY:
		result = SubqueryRef::Deserialize(deserializer);
		break;
	case TableReferenceType::TABLE_FUNCTION:
		result = TableFunctionRef::Deserialize(deserializer);
		break;
	default:
		throw SerializationException("Unsupported type for deserialization of TableRef!");
	}
	result->alias = std::move(alias);
	result->sample = std::move(sample);
	result->query_location = query_location;
	return result;
}

void BaseTableRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<string>(200, "schema_name", schema_name);
	serializer.WritePropertyWithDefault<string>(201, "table_name", table_name);
	serializer.WritePropertyWithDefault<vector<string>>(202, "column_name_alias", column_name_alias);
	serializer.WritePropertyWithDefault<string>(203, "catalog_name", catalog_name);
}

unique_ptr<TableRef> BaseTableRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<BaseTableRef>(new BaseTableRef());
	deserializer.ReadPropertyWithDefault<string>(200, "schema_name", result->schema_name);
	deserializer.ReadPropertyWithDefault<string>(201, "table_name", result->table_name);
	deserializer.ReadPropertyWithDefault<vector<string>>(202, "column_name_alias", result->column_name_alias);
	deserializer.ReadPropertyWithDefault<string>(203, "catalog_name", result->catalog_name);
	return std::move(result);
}

void ColumnDataRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<vector<string>>(200, "expected_names", expected_names);
	serializer.WritePropertyWithDefault<shared_ptr<ColumnDataCollection>>(202, "collection", collection);
}

unique_ptr<TableRef> ColumnDataRef::Deserialize(Deserializer &deserializer) {
	auto expected_names = deserializer.ReadPropertyWithDefault<vector<string>>(200, "expected_names");
	auto collection = deserializer.ReadPropertyWithDefault<shared_ptr<ColumnDataCollection>>(202, "collection");
	auto result = duckdb::unique_ptr<ColumnDataRef>(new ColumnDataRef(std::move(collection), std::move(expected_names)));
	return std::move(result);
}

void EmptyTableRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
}

unique_ptr<TableRef> EmptyTableRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<EmptyTableRef>(new EmptyTableRef());
	return std::move(result);
}

void ExpressionListRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<vector<string>>(200, "expected_names", expected_names);
	serializer.WritePropertyWithDefault<vector<LogicalType>>(201, "expected_types", expected_types);
	serializer.WritePropertyWithDefault<vector<vector<unique_ptr<ParsedExpression>>>>(202, "values", values);
}

unique_ptr<TableRef> ExpressionListRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<ExpressionListRef>(new ExpressionListRef());
	deserializer.ReadPropertyWithDefault<vector<string>>(200, "expected_names", result->expected_names);
	deserializer.ReadPropertyWithDefault<vector<LogicalType>>(201, "expected_types", result->expected_types);
	deserializer.ReadPropertyWithDefault<vector<vector<unique_ptr<ParsedExpression>>>>(202, "values", result->values);
	return std::move(result);
}

void JoinRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<unique_ptr<TableRef>>(200, "left", left);
	serializer.WritePropertyWithDefault<unique_ptr<TableRef>>(201, "right", right);
	serializer.WritePropertyWithDefault<unique_ptr<ParsedExpression>>(202, "condition", condition);
	serializer.WriteProperty<JoinType>(203, "join_type", type);
	serializer.WriteProperty<JoinRefType>(204, "ref_type", ref_type);
	serializer.WritePropertyWithDefault<vector<string>>(205, "using_columns", using_columns);
	serializer.WritePropertyWithDefault<bool>(206, "delim_flipped", delim_flipped);
	serializer.WritePropertyWithDefault<vector<unique_ptr<ParsedExpression>>>(207, "duplicate_eliminated_columns", duplicate_eliminated_columns);
}

unique_ptr<TableRef> JoinRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<JoinRef>(new JoinRef());
	deserializer.ReadPropertyWithDefault<unique_ptr<TableRef>>(200, "left", result->left);
	deserializer.ReadPropertyWithDefault<unique_ptr<TableRef>>(201, "right", result->right);
	deserializer.ReadPropertyWithDefault<unique_ptr<ParsedExpression>>(202, "condition", result->condition);
	deserializer.ReadProperty<JoinType>(203, "join_type", result->type);
	deserializer.ReadProperty<JoinRefType>(204, "ref_type", result->ref_type);
	deserializer.ReadPropertyWithDefault<vector<string>>(205, "using_columns", result->using_columns);
	deserializer.ReadPropertyWithDefault<bool>(206, "delim_flipped", result->delim_flipped);
	deserializer.ReadPropertyWithDefault<vector<unique_ptr<ParsedExpression>>>(207, "duplicate_eliminated_columns", result->duplicate_eliminated_columns);
	return std::move(result);
}

void PivotRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<unique_ptr<TableRef>>(200, "source", source);
	serializer.WritePropertyWithDefault<vector<unique_ptr<ParsedExpression>>>(201, "aggregates", aggregates);
	serializer.WritePropertyWithDefault<vector<string>>(202, "unpivot_names", unpivot_names);
	serializer.WritePropertyWithDefault<vector<PivotColumn>>(203, "pivots", pivots);
	serializer.WritePropertyWithDefault<vector<string>>(204, "groups", groups);
	serializer.WritePropertyWithDefault<vector<string>>(205, "column_name_alias", column_name_alias);
	serializer.WritePropertyWithDefault<bool>(206, "include_nulls", include_nulls);
}

unique_ptr<TableRef> PivotRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<PivotRef>(new PivotRef());
	deserializer.ReadPropertyWithDefault<unique_ptr<TableRef>>(200, "source", result->source);
	deserializer.ReadPropertyWithDefault<vector<unique_ptr<ParsedExpression>>>(201, "aggregates", result->aggregates);
	deserializer.ReadPropertyWithDefault<vector<string>>(202, "unpivot_names", result->unpivot_names);
	deserializer.ReadPropertyWithDefault<vector<PivotColumn>>(203, "pivots", result->pivots);
	deserializer.ReadPropertyWithDefault<vector<string>>(204, "groups", result->groups);
	deserializer.ReadPropertyWithDefault<vector<string>>(205, "column_name_alias", result->column_name_alias);
	deserializer.ReadPropertyWithDefault<bool>(206, "include_nulls", result->include_nulls);
	return std::move(result);
}

void ShowRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<string>(200, "table_name", table_name);
	serializer.WritePropertyWithDefault<unique_ptr<QueryNode>>(201, "query", query);
	serializer.WriteProperty<ShowType>(202, "show_type", show_type);
}

unique_ptr<TableRef> ShowRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<ShowRef>(new ShowRef());
	deserializer.ReadPropertyWithDefault<string>(200, "table_name", result->table_name);
	deserializer.ReadPropertyWithDefault<unique_ptr<QueryNode>>(201, "query", result->query);
	deserializer.ReadProperty<ShowType>(202, "show_type", result->show_type);
	return std::move(result);
}

void SubqueryRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<unique_ptr<SelectStatement>>(200, "subquery", subquery);
	serializer.WritePropertyWithDefault<vector<string>>(201, "column_name_alias", column_name_alias);
}

unique_ptr<TableRef> SubqueryRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<SubqueryRef>(new SubqueryRef());
	deserializer.ReadPropertyWithDefault<unique_ptr<SelectStatement>>(200, "subquery", result->subquery);
	deserializer.ReadPropertyWithDefault<vector<string>>(201, "column_name_alias", result->column_name_alias);
	return std::move(result);
}

void TableFunctionRef::Serialize(Serializer &serializer) const {
	TableRef::Serialize(serializer);
	serializer.WritePropertyWithDefault<unique_ptr<ParsedExpression>>(200, "function", function);
	serializer.WritePropertyWithDefault<vector<string>>(201, "column_name_alias", column_name_alias);
}

unique_ptr<TableRef> TableFunctionRef::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<TableFunctionRef>(new TableFunctionRef());
	deserializer.ReadPropertyWithDefault<unique_ptr<ParsedExpression>>(200, "function", result->function);
	deserializer.ReadPropertyWithDefault<vector<string>>(201, "column_name_alias", result->column_name_alias);
	return std::move(result);
}

} // namespace duckdb
