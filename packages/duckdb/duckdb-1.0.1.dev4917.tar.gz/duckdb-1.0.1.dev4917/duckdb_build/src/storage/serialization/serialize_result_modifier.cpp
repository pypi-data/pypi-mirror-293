//===----------------------------------------------------------------------===//
// This file is automatically generated by scripts/generate_serialization.py
// Do not edit this file manually, your changes will be overwritten
//===----------------------------------------------------------------------===//

#include "duckdb/common/serializer/serializer.hpp"
#include "duckdb/common/serializer/deserializer.hpp"
#include "duckdb/parser/result_modifier.hpp"
#include "duckdb/planner/bound_result_modifier.hpp"

namespace duckdb {

void ResultModifier::Serialize(Serializer &serializer) const {
	serializer.WriteProperty<ResultModifierType>(100, "type", type);
}

unique_ptr<ResultModifier> ResultModifier::Deserialize(Deserializer &deserializer) {
	auto type = deserializer.ReadProperty<ResultModifierType>(100, "type");
	unique_ptr<ResultModifier> result;
	switch (type) {
	case ResultModifierType::DISTINCT_MODIFIER:
		result = DistinctModifier::Deserialize(deserializer);
		break;
	case ResultModifierType::LIMIT_MODIFIER:
		result = LimitModifier::Deserialize(deserializer);
		break;
	case ResultModifierType::LIMIT_PERCENT_MODIFIER:
		result = LimitPercentModifier::Deserialize(deserializer);
		break;
	case ResultModifierType::ORDER_MODIFIER:
		result = OrderModifier::Deserialize(deserializer);
		break;
	default:
		throw SerializationException("Unsupported type for deserialization of ResultModifier!");
	}
	return result;
}

void BoundOrderModifier::Serialize(Serializer &serializer) const {
	serializer.WritePropertyWithDefault<vector<BoundOrderByNode>>(100, "orders", orders);
}

unique_ptr<BoundOrderModifier> BoundOrderModifier::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<BoundOrderModifier>(new BoundOrderModifier());
	deserializer.ReadPropertyWithDefault<vector<BoundOrderByNode>>(100, "orders", result->orders);
	return result;
}

void DistinctModifier::Serialize(Serializer &serializer) const {
	ResultModifier::Serialize(serializer);
	serializer.WritePropertyWithDefault<vector<unique_ptr<ParsedExpression>>>(200, "distinct_on_targets", distinct_on_targets);
}

unique_ptr<ResultModifier> DistinctModifier::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<DistinctModifier>(new DistinctModifier());
	deserializer.ReadPropertyWithDefault<vector<unique_ptr<ParsedExpression>>>(200, "distinct_on_targets", result->distinct_on_targets);
	return std::move(result);
}

void LimitModifier::Serialize(Serializer &serializer) const {
	ResultModifier::Serialize(serializer);
	serializer.WritePropertyWithDefault<unique_ptr<ParsedExpression>>(200, "limit", limit);
	serializer.WritePropertyWithDefault<unique_ptr<ParsedExpression>>(201, "offset", offset);
}

unique_ptr<ResultModifier> LimitModifier::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<LimitModifier>(new LimitModifier());
	deserializer.ReadPropertyWithDefault<unique_ptr<ParsedExpression>>(200, "limit", result->limit);
	deserializer.ReadPropertyWithDefault<unique_ptr<ParsedExpression>>(201, "offset", result->offset);
	return std::move(result);
}

void LimitPercentModifier::Serialize(Serializer &serializer) const {
	ResultModifier::Serialize(serializer);
	serializer.WritePropertyWithDefault<unique_ptr<ParsedExpression>>(200, "limit", limit);
	serializer.WritePropertyWithDefault<unique_ptr<ParsedExpression>>(201, "offset", offset);
}

unique_ptr<ResultModifier> LimitPercentModifier::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<LimitPercentModifier>(new LimitPercentModifier());
	deserializer.ReadPropertyWithDefault<unique_ptr<ParsedExpression>>(200, "limit", result->limit);
	deserializer.ReadPropertyWithDefault<unique_ptr<ParsedExpression>>(201, "offset", result->offset);
	return std::move(result);
}

void OrderModifier::Serialize(Serializer &serializer) const {
	ResultModifier::Serialize(serializer);
	serializer.WritePropertyWithDefault<vector<OrderByNode>>(200, "orders", orders);
}

unique_ptr<ResultModifier> OrderModifier::Deserialize(Deserializer &deserializer) {
	auto result = duckdb::unique_ptr<OrderModifier>(new OrderModifier());
	deserializer.ReadPropertyWithDefault<vector<OrderByNode>>(200, "orders", result->orders);
	return std::move(result);
}

} // namespace duckdb
