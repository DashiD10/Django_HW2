# Core Views Refactoring TODO

## Part 1: Simple TemplateView Classes ✅
- [x] Create `LandingView` class-based view
- [x] Create `ThanksView` class-based view
- [x] Update URL configuration to use new class-based views
- [x] Maintain existing functionality for context data

## Next Steps (Part 2-4):
- [ ] Refactor `orders_list` view to use `ListView`
- [ ] Refactor `order_detail` view to use `DetailView`
- [ ] Refactor `create_review` view to use `CreateView`
- [ ] Refactor `create_order` view to use `CreateView`
- [ ] Refactor `get_master_services` API endpoint
- [ ] Remove old function-based views once all refactored
- [ ] Update any remaining URL patterns

## Testing Checklist:
- [ ] Test landing page loads correctly with masters and reviews
- [ ] Test thanks page loads correctly
- [ ] Verify all existing functionality works as expected
- [ ] Check that context data is properly passed to templates
